import os
import sys
import time
import random
import datetime
import pyautogui
from psychopy import visual

FILE_NAME = "NO_NAME_PROVIDED"

# Check if a file name was provided
if (len(sys.argv) > 1):
    FILE_NAME = str(sys.argv[1])

# Get window size
try:
    SCREEN_WIDTH, SCREEN_HEIGHT = pyautogui.size()
except:
    print("pyautogui failed to capture screen size - please hardcode SCREEN_WIDTH, SCREEN_HEIGHT in code!")
    # Set your display size here
    SCREEN_WIDTH, SCREEN_HEIGHT = (600,360)

# Rotate data: SET THIS TO FALSE IF YOUR OUTPUT IS NOT MIRRORED
ROTATE_DATA = True

# Configuration parameters
REPETITIONS = 4
NUM_DIRECTIONS = 4
LENGTH_STIMULUS = 1
SCREEN_TO_USE = 0
TIME_BETWEEN_STIMULUS = 0

# Set up psychopy window based on monitor dimensions
WINDOW = visual.Window([SCREEN_WIDTH, SCREEN_HEIGHT], screen=SCREEN_TO_USE, monitor='testMonitor',
                    fullscr=False, color=[255,255,255], units='pix')

# Generate equally spaced directions between 0 and 360 degrees
DIRECTIONS = []
for i in range(NUM_DIRECTIONS):
    if i == 0:
        DIRECTIONS.append(0)
    else:
        DIRECTIONS.append(int(DIRECTIONS[i-1] + 360/NUM_DIRECTIONS))

if __name__ == "__main__":

    # Wait for keypress to begin
    input("Press any key to start")
    time_start = time.time()

    # Pick random direction from set of directions
    direction_to_use = random.choice(DIRECTIONS)

    # Loop for number of REPETITIONS
    for i in range(REPETITIONS):

        # Wait TIME_BETWEEN_STIMULUS seconds before showing stimulus
        time_start = time.time()
        while (time.time() - time_start) < TIME_BETWEEN_STIMULUS:
            print(f"{TIME_BETWEEN_STIMULUS - int(time.time() - time_start)} seconds until next exposure...")
            time.sleep(1)

        # Generate the GratingStim at dir degrees
        time_start = time.time()
        grat_stim = visual.GratingStim(win=WINDOW, tex='sqr', units='pix', pos=(0.0, 0.0), size=SCREEN_WIDTH*0.3, sf=0.02, ori=direction_to_use, phase=(0, 0))

        while True:
            grat_stim.phase += (0.01)
            grat_stim.draw()
            WINDOW.flip()
            if (time.time() - time_start) > LENGTH_STIMULUS:
                break

        # Clear the screen before next cycle
        WINDOW.flip()

    # If the file name already exists, just append the current time to the file name to avoid overwriting
    if os.path.isfile(f"{FILE_NAME}.txt"):
        FILE_NAME = FILE_NAME + "_" + str(int(time.time()))

    # New mapping: x -> (x + 180) % 360
    if ROTATE_DATA:
        direction_to_use = (direction_to_use + 180) % 360

    # Output our data to a file in the same directory
    with open(f"train-{FILE_NAME}.txt", "w") as fn:
        fn.write(f"Training - Date of test: {datetime.date.today()}\n\n")
        fn.write(f"Stimulus presented {REPETITIONS} times at {direction_to_use} degrees.")
