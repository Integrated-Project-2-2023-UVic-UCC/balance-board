from evdev import InputDevice, categorize, ecodes
from time import sleep
<<<<<<< HEAD
import serial

# Open serial port
ser= serial.Serial('/dev/ttyUSB0',9600)
try:
    gamepad = InputDevice('/dev/input/event4')
    button_pressed = False
    print("gamepad : ", gamepad)
except:
    print("Event not available")
    exit(0)

for event in gamepad.read_loop():
#     print(event)
    if event.type == ecodes.EV_KEY or event.type == ecodes.EV_ABS:
        if event.value == 1:
            button_pressed = True
            ser.write(str(event.code).encode())
        elif event.value == 0 and button_pressed:
            sleep(1)
            if event.code == 310:
                ser.write(str(10).encode())
            elif event.code == 311:
                ser.write(str(11).encode())

# close port
ser.close() 
=======


gamepad = InputDevice('/dev/input/event4')

x_btn = 307

for event in gamepad.read_loop():
    print("looping")
    if event.type == ecodes.EV_KEY or event.type == ecodes.EV_ABS:
        print("event code", event.code)
        if event.code == x_btn:
            print("X button pressed")
>>>>>>> bd2cb482064f0f0ba9242bf1842f64435736815f
