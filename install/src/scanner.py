import os, sys, signal
import board, busio
from digitalio import DigitalInOut
from adafruit_pn532.spi import PN532_SPI

# helpful constants:
CHAR_ID_BLOCK = 0x15

# keep track of last charID to prevent spam of same ID
lastCharID = None 

def handle_last_char_reset(signum, stack):
    global lastCharID

    lastCharID = None

def main(scanner_wr):
    global lastCharID

    # initialize SPI connection:
    spi = busio.SPI(board.SCK, board.MOSI, board.MISO)
    cs_pin = DigitalInOut(board.D5)
    pn532 = PN532_SPI(spi, cs_pin, debug=False)

    # configure PN532 to communicate with MiFare cards
    pn532.SAM_configuration()

    # handle last_char_reset signals from amiibrOS
    signal.signal(signal.SIGUSR1, handle_last_char_reset)

    # enter scanning loop:
    while True:
        # check if a card is available to read
        try:
            uid = pn532.read_passive_target(timeout=0.5)
        except RuntimeError:
            # this occurs when more than one card or incompatible card is detected.
            # tell amiibrOS that the scanned card could not be identified:
            pass #TODO remove and do as the above comment says
        
        # try again if no card is available
            if uid == None:
                continue

        try:
            charID = pn532.ntag2xx_read_block(CHAR_ID_BLOCK)
        except TypeError:
            # a bug in PN532_SPI will try to subscript a NoneType when the tag read
            #   becomes garbled (usually because a figure was lifted off of the
            #   scanner)
            continue # If this happens, we just try again.

        # try again if no ID is available
        if charID == None:
            continue

        # we are entering a critical section for lastCharID
        old_sigmask = signal.pthread_sigmask(signal.SIG_BLOCK, [signal.SIGUSR1])

        # tell amiibrOS the charID we found:
        if charID != lastCharID: # But only if it is not the same as previous
            lastCharID = charID
            os.write(scanner_wr, charID) # write data to the pipe
            os.kill(os.getppid(), signal.SIGUSR1) # tell parent that data is ready

        # exiting critical section for lastCharID
        signal.pthread_sigmask(signal.SIG_SETMASK, old_sigmask)

if __name__ == "__main__":
    # Note sys.argv[1] has the pipe's file descriptor if this program is called
    #   from amiibrOS.
    # retrieve the write-end of the pipe from amiibrOS
    scanner_wr = int(sys.argv[1])

    # initialize and begin scanning
    main(scanner_wr)
