# kvm_keys
# connect the uart ends into a hub
# connect the hid ends into each machine
# run this program.
# pick the port
# typing F12 is the escape sequence to exit back to the menu
# all keys will be sent to the selected

# specify --port /dev/serial/by-id/usb-FTDI_FT232R_USB_UART_A50285BI-if00-port0
# specify remote target system with --remote hostname
# in this mode it will capture the local keyboard and send the keystrokes
# via ssh to the remote system 

# when running as client
# it opens an ssh connection to the remote
# it copies the script there
# sets up the environment and runs it as role = server
#
# the local client handles usbhid-dump
# it creates usb strings and sends them to the server via the tunnel
#
# the server takes each message and sends it out the serial port

import fileinput
import serial
import queue
import time
import subprocess
import shlex
import os

def main(port = "/dev/serial/by-id/usb-FTDI_FT232R_USB_UART_A50285BI-if00-port0",
         remote = None,
         uid_vid = "03f0:034a",
         timeout = 5000,
         role = "client"):
    # use usbhid to grab keyboard

    #if remote:
        # generate a unique local port name
        #if not os.path.exists('/root/dev'):
        #    os.mkdir("/root/dev")
        #vmodem = f"/root/dev/{os.path.basename(port)}"
        #print(vmodem)
        # https://unix.stackexchange.com/questions/504621/use-remote-serial-port-as-a-local-one
        # dosen't work: serial.serialutil.SerialException: write failed: [Errno 5] Input/output error
        #cmd = f'socat PTY,link={vmodem},rawer,wait-slave EXEC:"ssh {remote} socat - {port},nonblock,rawer"'
        #cmd = shlex.split(cmd)
        #socat_proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        # it's remote, so pretend this is a local port
        #port = vmodem
        # wait till it should be ready
        #for i in range(10):
        #    if not os.path.exists(vmodem):
        #        print("waiting")
        #        time.sleep(1)
        #print("ready")
    # open the serial port
    ser = serial.Serial(port, baudrate=9600, timeout=0.5)

    # this script needs to also be on the remote side
    # this will copy the script to the remote side
    # set up the environment
    # run the server bit
    
    
    cmd = f"usbhid-dump -m {uid_vid} -es -t {timeout}"
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

    if remote:
        # close the remote serial port
        socat_proc.kill()

    time.sleep(2) # just to be sure all is cleaned up and it doesn't destablize the os

def server(port = "/dev/serial/by-id/usb-FTDI_FT232R_USB_UART_A50285BI-if00-port0"):
    # this runs on the machine with the usb serial port
    # open the serial port
    ser = serial.Serial(port, baudrate=9600, timeout=0.5)

    # read usbhid-dump data and parse it
    
    result = {}
    print("starting")
    while True:
    #for i in range(50):
        
        # https://stackoverflow.com/questions/1450393/how-do-you-read-from-stdin
        row = fileinput.input()
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

    

    

def codes_to_hid(codes):
    serial_data = serial.to_bytes(codes)
    return serial_data


if __name__ == '__main__':
    import typer
    typer.run(server)

