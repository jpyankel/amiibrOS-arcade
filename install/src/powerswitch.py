import threading, subprocess
import RPi.GPIO as GPIO
import os
import evdev

SHUTDOWN_HOLDTIME = 3.0 # Number of seconds we need to hold to shutdown
WAKE_PIN = 5 # GPIO Pin which we use for wake/shutdown functionality
EXIT_KEY = evdev.ecodes.KEY_ESC
KEYDOWN = 1
KEYUP = 0

def main():
    # use board pin numberings
    GPIO.setmode(GPIO.BOARD)
        
    # set wake pin to be an input pin pulled to high (3.3V)
    GPIO.setup(WAKE_PIN, GPIO.IN)

    # fake this device's capabilities, it should appear as a keyboard
    uinput = evdev.UInput.from_device("/dev/input/event0", name='powerswitch', vendor=0x413C, product=0x2501, version=0x111)

    while True:
        # wait for wake pin to be brought low
        GPIO.wait_for_edge(WAKE_PIN, GPIO.FALLING)
        uinput.write(evdev.ecodes.EV_KEY, EXIT_KEY, KEYDOWN)
        uinput.syn()

        # also start timer to perform shutdown after SHUTDOWN_HOLDTIME seconds
        shutdown_timer = threading.Timer(SHUTDOWN_HOLDTIME, shutdown)
        shutdown_timer.start()

        # wait until user releases switch
        GPIO.wait_for_edge(WAKE_PIN, GPIO.RISING)

        # cancel our previous shutdown timer if it hasn't shutdown yet
        shutdown_timer.cancel()

        # record as an ESC key press
        uinput.write(evdev.ecodes.EV_KEY, EXIT_KEY, KEYUP)
        uinput.syn()

def shutdown():
    # Best practice to perform cleanup before program termination:
    GPIO.cleanup()

    # Shutdown:
    subprocess.call('poweroff', shell=False)

if __name__ == '__main__':
    main()