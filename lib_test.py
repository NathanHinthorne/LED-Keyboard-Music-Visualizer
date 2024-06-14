from openrgb import OpenRGB
import time
import random

client = OpenRGB('localhost', 6742) # open connection on port 6742 (OpenRGB default port)

devices = client.devices()

# get only the keyboard device
keyboard = next(devices)
print('{} has {} LEDs'.format(keyboard.name, len(keyboard.leds)))

led_ids = [31, 30, 29, 28, 27, 26, 25, 24, 23, 22, 
           52, 51, 50, 49, 48, 47, 46, 45, 44, 43, 
           73, 72, 71, 70, 69, 68, 67, 66, 65, 64,
           95, 94, 93, 92, 91, 90, 89, 88, 87, 86]


curr_led_index = 0
while curr_led_index < len(led_ids):
    ledID = led_ids[curr_led_index]
    # keyboard.leds[ledID].set((255, 0, 0))
    client.update_single_led(ledID, (255, 0, 0))
    time.sleep(0.3)
    curr_led_index += 1