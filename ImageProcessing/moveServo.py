# servo move simple
from gpiozero import Servo
from time import sleep
from gpiozero.pins.pigpio import PiGPIOFactory

pigpio_factory = PiGPIOFactory()
servo1 = Servo(17,pin_factory=pigpio_factory)
servo2 = Servo(18,pin_factory=pigpio_factory)

while True:
 servo1.value = 0.05
 servo2.value = 0
 print(f"Servo 1= {servo1.value:4.1f}; Servo 2 = {servo2.value:4.1f}")