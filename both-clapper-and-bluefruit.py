# By John Gallaugher https://gallaugher.com  Twitter: @gallaugher
# YouTube: https://YouTube.com/profgallaugher
# Step-by-step video playlist demonstrating build at: https://bit.ly/bluefruit-school

# Run into build trouble? Adafruit runs a great help forum at:
# https://forums.adafruit.com - most questions are answered within an hour.
# Adafruit also has a discord channel at:
# http://adafru.it/discord

import board
import neopixel
import time
from adafruit_circuitplayground import cp

# imports needed for bluetooth
import digitalio
from adafruit_ble import BLERadio
from adafruit_ble.advertising.standard import ProvideServicesAdvertisement
from adafruit_ble.services.nordic import UARTService
from adafruit_bluefruit_connect.packet import Packet
from adafruit_bluefruit_connect.color_packet import ColorPacket
from adafruit_bluefruit_connect.button_packet import ButtonPacket

# set up the relay
relay = digitalio.DigitalInOut(board.A1)
relay.direction = digitalio.Direction.OUTPUT

# Set initial number of claps detected to zero
number_of_claps = 0
# adjust sound_threshold lower to detect softer claps
# or higher to detect only louder claps
# It's a good idea to test on background noise or talking voice / laughter
# from the distance people are likely to be from the CPB.
sound_threshold = 1500
time_at_last_clap = time.monotonic()

# Note: this code is improved over code in original video
time_at_last_clap = time.monotonic()

# setup bluetooth
ble = BLERadio()
uart_server = UARTService()
advertisement = ProvideServicesAdvertisement(uart_server)
# Give your CPB a unique name between the quotes below
advertisement.complete_name = "Lamp"

def respond_to_claps(time_at_last_clap, number_of_claps):
    if cp.loud_sound(sound_threshold): # loud sound detected
        time_at_last_clap = time.monotonic() # record time since last clap
        number_of_claps = number_of_claps + 1 # add one to number_of_claps
        if number_of_claps > 1: # if a more than one clap in a row
            relay.value = not relay.value # if off, turn on, if on, turn off
            number_of_claps = 0 # set number_of_claps back down to zero.
        time.sleep(0.2)
    else: # time has passed without a loud sound detected
        time_since_last_clap = time.monotonic() - time_at_last_clap
        if time_since_last_clap > 1: # if one second has gone by since last clap, reset clap count to zero
            number_of_claps = 0 # reset number_of_claps back to zero.
    return time_at_last_clap, number_of_claps

while True:
    ble.start_advertising(advertisement)
    while not ble.connected:
        time_at_last_clap, number_of_claps = respond_to_claps(time_at_last_clap, number_of_claps)

    # Now we're connected so we don't need to advertise the device as one that you're able to connect to
    ble.stop_advertising()

    while ble.connected:
        time_at_last_clap, number_of_claps = respond_to_claps(time_at_last_clap, number_of_claps)
        if uart_server.in_waiting:
            try:
                packet = Packet.from_stream(uart_server)
            except ValueError:
                continue # or pass. This will start the next

            if isinstance(packet, ColorPacket):
                pass

            if isinstance(packet, ButtonPacket):
                if packet.pressed:
                    if packet.button == ButtonPacket.BUTTON_1:
                        relay.value = not relay.value
                    elif packet.button == ButtonPacket.BUTTON_2:
                        pass
                    elif packet.button == ButtonPacket.BUTTON_3:
                        pass
                    elif packet.button == ButtonPacket.BUTTON_4:
                        pass
                    elif packet.button == ButtonPacket.UP:
                        pass
                    elif packet.button == ButtonPacket.DOWN:
                        pass
                    elif packet.button == ButtonPacket.RIGHT:
                        pass
                    elif packet.button == ButtonPacket.LEFT:
                        pass
    # If we got here, we lost the connection. Go up to the top and start
    # advertising again and waiting for a connection.
