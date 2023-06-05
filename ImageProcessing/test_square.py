import RPi.GPIO as GPIO
import time

servo_pin = 17
GPIO.setmode(GPIO.BCM)
GPIO.setup(servo_pin, GPIO.OUT)


pwm = GPIO.PWM(servo_pin, 50)

angulo_inicio = 0
angulo_fin = 180

rango_angulo = angulo_fin - angulo_inicio
rango_pwm = 12.5
paso = rango_pwm / rango_angulo

def establecer_angulo(angulo):
    duracion_pulso = 2.5 + (angulo * paso)
    pwm.ChangeDutyCycle(duracion_pulso)
    
try:

     pwm.start(2.5)
#     while True:
        
#     while True:
#         for angulo in range(angulo_inicio, angulo_fin +1):
#             establecer_angulo(angulo)
#             time.sleep(0.01)
#             
#         for angulo in range(angulo_fin, angulo_inicio -1, -1):
#             establecer_angulo(angulo)
#             time.sleep(0.01)

except KeyboardInterrupt:
    pwm.stop()
    GPIO.cleanup()