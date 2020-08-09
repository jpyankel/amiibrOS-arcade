import pygame, os, sys, signal
from pathlib import Path
from input_manager import InputManager
from state_engine import StateEngine
from draw_manager import DrawManager

# configurations
DRAW_FPS_OVERLAY = True
UI_DEVELOPMENT = False

# consts
CHAR_ID_LEN = 8
BYTES_PER_CHAR_ID = CHAR_ID_LEN >> 1

# path to amiibrOS folder; various images/fonts are stored here
root_path = (Path(__file__).parent.parent).resolve()
app_path = root_path / "app"
src_path = root_path / "src"

def main(scanner_pid, switch_pid, scanner_re):
    user_exit = False

    while not user_exit:
        # we are the parent process in this function

        # start by initializing UI
        pygame.init()
        input_mgr = InputManager()
        state_eng = StateEngine()
        draw_mgr = DrawManager()
        clock = pygame.time.Clock()

        scanner_bytes_to_read = BYTES_PER_CHAR_ID
        data = bytearray()

        while not (input_mgr.keyboard_forcequit or state_eng.scan_success):
            # limit frontend graphics and logic to roughly 60 Hz
            dt = clock.tick(60)/1000.0

            # --- Main Loop ---
            # read up to 8 bytes from scanner pipe
            try:
                new_bytes = bytearray(os.read(scanner_re, scanner_bytes_to_read))
                bytes_read = len(new_bytes)
                data += new_bytes
                scanner_bytes_to_read -= bytes_read
                if scanner_bytes_to_read == 0:
                    # convert data to charID hex string
                    charID = data.hex()
                    # preupdate input_mgr with the charID we read
                    input_mgr.scan(charID)
                    # reset # of bytes and data for reading next frame
                    scanner_bytes_to_read = BYTES_PER_CHAR_ID
                    data = bytearray()
            except BlockingIOError:
                # this occurs when no data is being written into the pipe from the scanner
                # just ignore and move on
                pass

            # update inputs, this will automatically set flags we need to check for main logic
            input_mgr.update(dt)

            # now do main logic depending on state
            state_eng.update(input_mgr, draw_mgr)

            # now draw updated scene objects to the screen
            draw_mgr.update(dt, clock.get_fps() if DRAW_FPS_OVERLAY else None)

            # -----------------
        
        if input_mgr.keyboard_forcequit:
            # user exited pygame interface and wants to do debugging stuff without amiibrOS active
            # first, tell scanner to exit
            os.kill(scanner_pid, signal.SIGTERM)
            # wait for scanner to terminate
            os.waitpid(scanner_pid, 0)
            # close scanner pipe
            os.close(scanner_re)
            # kill and wait for the powerswitch program to end
            os.kill(switch_pid, signal.SIGTERM)
            os.waitpid(switch_pid, 0)
            # finish exiting
            user_exit = True
        elif state_eng.scan_success:
            # an NFC figure was scanned successfully
            # grab charID value from the state_engine
            charID = state_eng.success_char_id

            # get the app to run and run it
            app_folder = app_path/charID      # scan_success guarantees this folder exists
            app = app_folder/(charID + ".sh") # and this file too

            # pygame deinit, cleanup, etc.
            input_mgr.reset()
            state_eng.reset()
            draw_mgr.reset()
            pygame.quit()

            # launch the process indicated by charID
            app_pid = os.fork()
            if not app_pid:
                # close the scanner output pipe for the child process
                os.close(scanner_re)

                # we are the child process, execute the .sh file in the figure's folder
                os.execv("/bin/sh", ["sh", app])
            
            # wait until the process dies and then show amiibrOS again
            os.waitpid(app_pid, 0)

# this function is for testing and develop the UI only.
# it is like main(), but replaces or removes all functionalities that a regular PC can't accommodate
def testmain():
    pygame.init()
    input_mgr = InputManager()
    state_eng = StateEngine()
    draw_mgr = DrawManager()
    clock = pygame.time.Clock()

    while not input_mgr.keyboard_forcequit:
        # limit frontend graphics and logic to roughly 60 Hz
        dt = clock.tick(60)/1000.0

        # --- Main Loop ---

        # update inputs, this will automatically set flags we need to check for main logic
        input_mgr.update(dt)

        # now do main logic depending on state
        state_eng.update(input_mgr, draw_mgr)

        # now draw updated scene objects to the screen
        draw_mgr.update(dt, clock.get_fps() if DRAW_FPS_OVERLAY else None)

        # -----------------

if __name__ == "__main__":
    if UI_DEVELOPMENT:
        testmain()
        sys.exit()

    # fork the power-switch monitor process
    switch_pid = os.fork()

    if not switch_pid:
        # make the child process execute the powerswitch monitor
        os.execv(sys.executable, ["python3", (src_path/"powerswitch.py").resolve()])

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

    main(scanner_pid, switch_pid, scanner_re)