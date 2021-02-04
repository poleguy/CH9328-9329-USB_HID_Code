# kvm_keys
# connect the uart ends into a hub
# connect the hid ends into each machine
# run this program.
# pick the port
# typing F12 is the escape sequence to exit back to the menu
# all keys will be sent to the selected 
import serial
import queue
import time
import subprocess
import shlex

def main(port = "/dev/serial/by-id/usb-FTDI_FT232R_USB_UART_A50285BI-if00-port0"):
    # use usbhid to grab keyboard
    ser = serial.Serial(port, baudrate=9600, timeout=0.5)

    cmd = "usbhid-dump -m 03f0:034a -es -t 5000"
    cmd = shlex.split(cmd)
    proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    result = {}
    while True:
    #for i in range(50):
        row = proc.stdout.readline()
        if row == b'':
            print("timeout detected")
            break
        print(row)
        print('row done')
        if b'STREAM' in row:
            print('...')
            values = proc.stdout.readline().decode("utf-8")
            print(values)
            values = values.split(' ')
            codes = []
            for v in values[1:]:
                code = int(v, 16)
                codes.append(code)
            print(codes)
            serial_data = codes_to_hid(codes)
            if codes == [0,0,0x45,0,0,0,0,0]:
                print('F12 pressed... ending session.')
                break
            print('.')
            ser.write(serial_data)
    print('done')
    # wait till timeout
    proc.communicate()

    time.sleep(2) # just to be sure all is cleaned up and it doesn't destablize the os



def codes_to_hid(codes):
    serial_data = serial.to_bytes(codes)
    return serial_data


if __name__ == '__main__':
    main()

