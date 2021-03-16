import os
import sys
import time
import numpy
import random
import datetime
import pyautogui
from psychopy import visual, core, event

FILE_NAME = "NO_NAME_PROVIDED"

# Check if a file name was provided
if (len(sys.argv) > 2):
    FILE_NAME = str(sys.argv[1])

# Get window size
SCREEN_WIDTH, SCREEN_HEIGHT = pyautogui.size()

# Configuration parameters
TESTS = 3
CYCLES = 8
EXPOSURE_TIME = 5
SCREEN_TO_USE = 0
TIME_BETWEEN_EXPOSURES = 20

# Set up psychopy window based on monitor dimensions
WINDOW = visual.Window([SCREEN_WIDTH, SCREEN_HEIGHT], screen=SCREEN_TO_USE, monitor='testMonitor',
                    fullscr=False, color=[255,255,255], units='pix')

# Generate equally spaced directions between 0 and 360 degrees
DIRECTIONS = []
for i in range(CYCLES):
    if i == 0:
        DIRECTIONS.append(0)
    else:
        DIRECTIONS.append(int(DIRECTIONS[i-1] + 360/CYCLES))

if __name__ == "__main__":

    # Order of cycles
    cycles = []

    # Wait for keypress to begin
    input("Press any key to start")
    time_start = time.time()

    # Loop for number of tests
    for i in range(TESTS):

        # Randomize the sequence of directions for the test
        random.shuffle(DIRECTIONS)

        # Loop for number of cycles
        for dir in DIRECTIONS:

            # Wait TIME_BETWEEN_EXPOSURES seconds before showing stimulus
            time_start = time.time()
            while (time.time() - time_start) < TIME_BETWEEN_EXPOSURES:
                print(f"{TIME_BETWEEN_EXPOSURES - int(time.time() - time_start)} seconds until next exposure...")
                time.sleep(1)

            # Generate the GratingStim at dir degrees
            time_start = time.time()
            grat_stim = visual.GratingStim(win=WINDOW, tex='sqr', units='pix', pos=(0.0, 0.0), size=SCREEN_WIDTH*0.3, sf=0.02, ori=dir, phase=(0, 0))

            while True:
                grat_stim.phase += (0.01)
                grat_stim.draw()
                WINDOW.flip()
                if (time.time() - time_start) > EXPOSURE_TIME:
                    break

            # Clear the screen before next cycle
            WINDOW.flip()

        # Output order of cycle
        cycles.append(DIRECTIONS)

    # If the file name already exists, just append the current time to the file name to avoid overwriting
    if os.path.isfile(f"{FILE_NAME}.txt"):
        FILE_NAME = FILE_NAME + "_" + str(int(time.time()))

    # Output our data to a file in the same directory
    with open(f"{FILE_NAME}.txt", "w") as fn:
        fn.write(f"Date of test: {datetime.date.today()}\n\n")
        fn.write("Stimulus presented in the following order:\n\n")
        for block in cycles:
            for degree in block:
                fn.write(str(degree) + "\n")
