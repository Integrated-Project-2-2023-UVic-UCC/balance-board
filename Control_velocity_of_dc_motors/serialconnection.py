import serial

# Open serial port
ser= serial.Serial('/dev/ttyUSB0',9600)

number = 105
ser.write(str(number).encode())

# close port
ser.close() 