from time import sleep
import pigpio

import gpiozero
from gpiozero.pins.pigpio import PiGPIOFactory
#gpiozero.Device.pin_factory = pigpio.pi()
pigpio_factory = PiGPIOFactory()


angle1 = 0
value = -0.0

s = gpiozero.AngularServo(17,min_angle=-90, max_angle=90, min_pulse_width=0.0005, max_pulse_width=0.0025,pin_factory=pigpio_factory)

value = (((value + 0.8) * 115) / 1.6)-65
print(value)

s.angle = value
sleep(5)


s.detach()