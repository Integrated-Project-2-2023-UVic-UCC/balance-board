from pyPS4Controller.controller import Controller
import serial

# Open serial port
ser= serial.Serial('/dev/ttyUSB0',9600)

class MyController(Controller):
    def __init__(self, **kwargs):
        Controller.__init__(self, **kwargs)
    def on_triangle_press(self):
        print("Forward")
        ser.write(str(307).encode())
    def on_x_press(self):
        print("Backward")
        ser.write(str(304).encode())
    def on_R3_up(self, value):
        print("Stop left")
        ser.write(str(312).encode())
    def on_R3_left(self, value):
        print("Stop right")
        ser.write(str(313).encode())
    def on_L1_press(self):
        print("turn left")
        ser.write(str(310).encode())
    def on_L1_release(self):
        print("stop turn left")
        ser.write(str(10).encode())
    def on_R1_press(self):
        print("turn right")
        ser.write(str(311).encode())
    def on_R1_release(self):
        print("stop turn right")
        ser.write(str(11).encode())
controller = MyController(interface="/dev/input/js0", connecting_using_ds4drv=True)

controller.listen()