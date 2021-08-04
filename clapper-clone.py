# IMPORTANT NOTE: This code only works on a CPB, not a CPX
# That's because the chip used in the CPX (The SAMD21) cannot
# handle the sound sensor features in the cp library that the
# more powerful chip in the CPB (nRF52840) can.

import time
import board
from adafruit_circuitplayground import cp
import digitalio

# set up the relay
relay = digitalio.DigitalInOut(board.A1)
relay.direction = digitalio.Direction.OUTPUT

# Set initial number of claps detected to zero
number_of_claps = 0
# adjust sound_threshold lower to detect softer claps
# or higher to detect only louder claps
# It's a good idea to test on background noise or talking voice / laughter
# from the distance people are likely to be from the CPB.
sound_threshold = 250

while True:
    if cp.loud_sound(sound_threshold): # loud sound detected
        print((cp.sound_level,)) # will print to Plotter if you want to see the plot
        number_of_claps = number_of_claps + 1 # add one to number_of_claps
        print("*** Clap! #:", number_of_claps)
        if number_of_claps > 1: # if a more than one clap in a row
            if relay.value: # If relay.value == True then lights are on, so set to off
                relay.value = False # lights are off, relay is closed
                cp.pixels.fill((0, 0, 0)) # you can delete if you don't want LEDs on CPB to flash w/the lamp connected to the relay
                print("Lights Are Off!")
            else: # relay.value must be False ,so...
                relay.value = True # change relay.value to True, that turns on lamp connected to relay switch
                cp.pixels.fill((50, 0, 50))
                print("Lights Are On!")
            number_of_claps = 0 # set number_of_claps back down to zero.
        time.sleep(0.2)
    else: # time has passed without a loud sound detected
        print((cp.sound_level,)) # will print to Plotter if you want to see the plot
        number_of_claps = 0 # reset number_of_claps back to zero.
        print("No claps", number_of_claps)

