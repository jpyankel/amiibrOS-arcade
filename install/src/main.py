import pygame, os, sys, signal
from pathlib import Path
import configparser
from input_manager import InputManager
from state_engine import StateEngine
from draw_manager import DrawManager

# configurations
DRAW_FPS_OVERLAY = False

# consts
CHAR_ID_LEN = 8
BYTES_PER_CHAR_ID = CHAR_ID_LEN >> 1

# path to amiibrOS folder; various images/fonts are stored here
root_path = (Path(__file__).parent.parent).resolve()
app_path = root_path / "app"
src_path = root_path / "src"
data_path = root_path / "data"
controller_path = data_path / "gamepads.config"

# === Globals ===
# flags and data for scanner
scanner_data_ready = False
scanner_data = bytearray()
scanner_re = None # read end of scanner pipe

def handle_scanner(signum, stack):
    global scanner_data_ready, scanner_data, scanner_re

    # if scanner_data_ready (we haven't handled it yet), replace old data with the latest
    if scanner_data_ready == True:
        scanner_data = bytearray()

    # will will be reading 4 bytes from scanner pipe
    scanner_bytes_to_read = BYTES_PER_CHAR_ID

    # read the bytes and tell input_mgr at the start of the next loop
    while scanner_bytes_to_read != 0:
        try:
            new_bytes = bytearray(os.read(scanner_re, scanner_bytes_to_read))
            bytes_read = len(new_bytes)
            scanner_data += new_bytes
            scanner_bytes_to_read -= bytes_read
        except BlockingIOError:
            # this occurs when no data is being written into the pipe from the scanner
            # just ignore and move on
            pass
    
    scanner_data_ready = True

def main(scanner_pid):
    # we are the parent process in this function
    global scanner_data_ready, scanner_data, scanner_re

    # --- one time setup ---
    # load joystick config files from data/controllers.config
    gamepadConfigs = configparser.ConfigParser()
    with open(str(controller_path)) as conf:
        gamepadConfigs.read_file(conf)

    # enable handling of scanner-data-ready signal (SIGUSR1)
    signal.signal(signal.SIGUSR1, handle_scanner)
    # --- ---

    while True:
        # start by initializing pygame UI
        pygame.init()
        input_mgr = InputManager(gamepadConfigs)
        state_eng = StateEngine()
        draw_mgr = DrawManager()
        clock = pygame.time.Clock()

        # hide mouse
        pygame.mouse.set_visible(False)

        while not (state_eng.scan_success or state_eng.exit_ready):
            # limit frontend graphics and logic to roughly 60 Hz
            dt = clock.tick(60)/1000.0

            # --- Main Loop ---
            # disable scanner interrupts during the main loop
            signal.pthread_sigmask(signal.SIG_BLOCK, [signal.SIGUSR1])

            # handle scanner input
            if scanner_data_ready:
                # we have a charID!
                # convert data to charID hex string
                charID = scanner_data.hex()
                # preupdate input_mgr with the charID we read
                input_mgr.scan(charID)
                # reset data for future reads
                scanner_data = bytearray()
                scanner_data_ready = False

            # handle powerswitch/keyboard escape input
            if not state_eng.exiting and input_mgr.keyboard_forcequit:
                state_eng.exit_sequence(input_mgr, draw_mgr)

            # update other inputs, this will automatically set flags we need to check for main logic
            input_mgr.update(dt)

            # now do main logic depending on state
            state_eng.update(input_mgr, draw_mgr)

            # now draw updated scene objects to the screen
            draw_mgr.update(dt, clock.get_fps() if DRAW_FPS_OVERLAY else None)

            # re-enable scanner interrupts if we are remaining in the menus
            if not (state_eng.scan_success or state_eng.exiting):
                signal.pthread_sigmask(signal.SIG_UNBLOCK, [signal.SIGUSR1])

            # -----------------

        # we have exited the main loop for one of two reasons
        if state_eng.exit_ready:
            # user exited pygame interface and wants to do debugging stuff without amiibrOS active
            amiibrOS_exit(scanner_pid, scanner_re)
        elif state_eng.scan_success:
            # an NFC figure was scanned successfully
            # grab charID value from the state_engine
            charID = state_eng.success_char_id

            # pygame deinit, cleanup, etc.
            input_mgr = None
            state_eng = None
            draw_mgr = None
            clock = None
            pygame.quit()

            # get the app to run and run it
            app_folder = app_path/charID      # scan_success guarantees this folder exists
            app = app_folder/(charID + ".sh") # and this file too

            # launch the process indicated by charID
            app_pid = os.fork()
            if not app_pid:
                # close the scanner output pipe for the child process
                os.close(scanner_re)

                # we are the child process, execute the .sh file in the figure's folder
                os.execv("/bin/sh", ["sh", app])
            
            # wait until the process dies and then show amiibrOS again
            os.waitpid(app_pid, 0)
        
            # reset code ---
            # in case we have an NFC scan or exit request pending, clear it now
            signal.signal(signal.SIGUSR1, signal.SIG_IGN) # ignoring the signal and then ...
            signal.pthread_sigmask(signal.SIG_UNBLOCK, [signal.SIGUSR1]) # ... unblocking clears it

            # at this point, we also want to allow the user to re-scan the same NFC figure they used
            #   before. To accomplish this, we send a SIGUSR1 signal to scanner
            os.kill(scanner_pid, signal.SIGUSR1)

            signal.signal(signal.SIGUSR1, handle_scanner) # reset the signal handler

def amiibrOS_exit(scanner_pid, scanner_re):
    # first, tell scanner to exit
    os.kill(scanner_pid, signal.SIGTERM)
    # wait for scanner to terminate
    os.waitpid(scanner_pid, 0)
    # close scanner pipe
    os.close(scanner_re)
    # finish exiting
    sys.exit()

if __name__ == "__main__":
    # set up a pipe for communication with the scanner process (scanner writes, parent reads)
    # it is required to be non-blocking since we read while the UI is running in real time
    scanner_re, scanner_wr = os.pipe2(os.O_NONBLOCK)

    # fork the scanner process
    scanner_pid = os.fork()

    if not scanner_pid:
        # close the unused read-end of the pipe for the child process
        os.close(scanner_re)
        # we are the child process now
        # launch the scanner program, send it the write-end of the pipe
        os.execv(sys.executable, ["python3", (src_path/"scanner.py").resolve(), str(scanner_wr)])

    # close the unused write-end of the pipe (for the parent)
    os.close(scanner_wr)

    main(scanner_pid)