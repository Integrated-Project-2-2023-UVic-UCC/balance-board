# Script that runs in a loop until device is connected

import subprocess

cmd1 = "/bin/echo -e 'connect 98:B6:E9:C1:17:DE' | bluetoothctl"
cmd2 = "/bin/echo -e 'paired-devices' | bluetoothctl"
msg = "Device 98:B6:E9:C1:17:DE Wireless Controller"

while True:
    
    process = subprocess.Popen(cmd1, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output , error = process.communicate()

    if process.returncode == 0:
        con_process = subprocess.Popen(cmd2, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        con_output , con_error = con_process.communicate()
        res = con_output.decode()
        val = res.find(msg)
        if (val >= 0):
            print("Device is connected")
            break
        else:
            print("Try again")
    else:
        print(error.decode())
