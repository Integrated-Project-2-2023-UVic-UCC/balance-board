from evdev import InputDevice, categorize, ecodes
from time import sleep


gamepad = InputDevice('/dev/input/event4')

x_btn = 307

for event in gamepad.read_loop():
    print("looping")
    if event.type == ecodes.EV_KEY or event.type == ecodes.EV_ABS:
        print("event code", event.code)
        if event.code == x_btn:
            print("X button pressed")