from evdev import InputDevice, categorize, ecodes
from time import sleep
import serial

# Open serial port
ser= serial.Serial('/dev/ttyUSB0',9600)

gamepad = InputDevice('/dev/input/event4')
button_pressed = False

for event in gamepad.read_loop():
    if event.type == ecodes.EV_KEY or event.type == ecodes.EV_ABS:
        if event.value == 1:
            button_pressed = True
            print("pressed", event.code)
            ser.write(str(event.code).encode())
        elif event.value == 0 and button_pressed:
            print("released", event.code)
#             ser.write(str(event.code).encode())

# close port
ser.close() 