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

# setup bluetooth
ble = BLERadio()
uart_server = UARTService()
advertisement = ProvideServicesAdvertisement(uart_server)
# Give your CPB a unique name between the quotes below
advertisement.complete_name = "Lamp"

while True:
    ble.start_advertising(advertisement)
    while not ble.connected:
        pass

    # Now we're connected so we don't need to advertise the device as one that you're able to connect to
    ble.stop_advertising()

    while ble.connected:
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
