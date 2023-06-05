# Script that runs in a loop until device is connected
from evdev import InputDevice, categorize, ecodes
from time import sleep
import serial
import subprocess

cmd1 = "/bin/echo -e 'connect 98:B6:E9:C1:17:DE' | bluetoothctl"
cmd2 = "/bin/echo -e 'paired-devices' | bluetoothctl"
cmd3 = "sudo systemctl start joystickEvents.service"
cmd4 = "sudo systemctl stop joystickEvents.service"
cmd5 = "ls /dev/input"
msg = "Device 98:B6:E9:C1:17:DE Wireless Controller"
isOn = False

def check_event():
    con_process = subprocess.Popen(cmd5, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    con_output , con_error = con_process.communicate()
    res = con_output.decode()
    return res

joystick_process = subprocess.Popen(cmd4, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
while True:
    
    process = subprocess.Popen(cmd1, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output , error = process.communicate()

    if process.returncode == 0:
        con_process = subprocess.Popen(cmd2, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        con_output , con_error = con_process.communicate()
        res = con_output.decode()
        val = res.find(msg)
        if (val >= 0 and isOn == False):
            print("Device is connected first time")
            res = check_event()
            val = res.find("event4")
            if (val):
                print("Found event")
                joystick_process = subprocess.Popen(cmd3, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                isOn = True
            else:
                res = check_event()
                joystick_process = subprocess.Popen(cmd3, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                isOn = True
        elif (isOn == True):
            print("Device is connected")
        else:
            print("Try again")
    else:
        print(error.decode())
