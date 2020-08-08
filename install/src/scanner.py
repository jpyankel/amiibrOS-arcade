import os
import sys
import board
import busio
from digitalio import DigitalInOut
from adafruit_pn532.spi import PN532_SPI

# Helpful constants:
CHAR_ID_BLOCK = 0x15

def main(scanner_wr):
    # Initialize SPI connection:
    spi = busio.SPI(board.SCK, board.MOSI, board.MISO)
    cs_pin = DigitalInOut(board.D5)
    pn532 = PN532_SPI(spi, cs_pin, debug=False)

    # Configure PN532 to communicate with MiFare cards
    pn532.SAM_configuration()

    lastCharID = None # Keep track of last charID to prevent spam of same ID

    # Enter scanning loop:
    while True:
        # Check if a card is available to read
        try:
            uid = pn532.read_passive_target(timeout=0.5)
        except RuntimeError:
            # This occurs when more than one card or incompatible card is detected.
            # Tell amiibrOS that the scanned card could not be identified:
            pass #TODO Remove and do as the above comment says
        
        # Try again if no card is available
            if uid == None:
                continue

        try:
            charID = pn532.ntag2xx_read_block(CHAR_ID_BLOCK)
        except TypeError:
            # A bug in PN532_SPI will try to subscript a NoneType when the tag read
            #   becomes garbled (usually because an amiibo was lifted off of the
            #   scanner)
            continue # If this happens, we just try again.

        # Try again if no ID is available
        if charID == None:
            continue

        # Tell amiibrOS the charID we found:
        if charID != lastCharID: # But only if it is not the same as previous
            lastCharID = charID
            os.write(scanner_wr, charID)

if __name__ == "__main__":
    # Note sys.argv[1] has the pipe's file descriptor if this program is called
    #   from amiibrOS.
    # retrieve the write-end of the pipe from amiibrOS
    scanner_wr = int(sys.argv[1])

    # initialize and begin scanning
    main(scanner_wr)
