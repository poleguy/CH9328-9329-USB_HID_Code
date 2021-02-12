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
# See http://pexpect.sourceforge.net/
import pexpect
from pexpect import pxssh


def main(port = "/dev/serial/by-id/usb-FTDI_FT232R_USB_UART_A50285BI-if00-port0",
         remote = None,
         username = None,
         uid_vid = "03f0:034a",
         timeout = 5000,
         role = "server"):
    # use usbhid to grab keyboard

    if "server" in role:
        server(port=port)
        return

    # running locally.
    # grab keyboard

    if remote:
        # https://pexpect.readthedocs.io/en/stable/api/pxssh.html
        p = pxssh.pxssh()
        p.login(remote, username)
        p.sendline('source activate')
        p.prompt()
        print(p.before)
        
        p.sendline('conda activate ~/CH9328-9329-USB_HID_Code/cenv')
        p.prompt()
        print(p.before)
        p.sendline('python CH9328-9329-USB_HID_Code/kvm_keys.py')
        p.expect('kvm_keys> ')
        
    cmd = f"usbhid-dump -m {uid_vid} -es -t {timeout}"
    print(cmd)
    cmd = shlex.split(cmd)
    proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    # also open ssh connection
    #cmd = f'ssh dietzn@debussy.shurelab.com "source activate && conda activate ~/CH9328-9329-USB_HID_Code/cenv && echo blah && python3 CH9328-9329-USB_HID_Code/kvm_keys.py"'
    #cmd = shlex.split(cmd)
    #ssh_proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)


    result = {}
    while True:
    #for i in range(50):
        raw_row = proc.stdout.readline()
        row = raw_row.decode('utf-8').strip('\n')

        print(raw_row)
        if raw_row == b'':            
            print("timeout detected with 'b'",flush=True)
            p.sendline('No more')
            p.prompt()
            print(f"far end: {p.before.decode('utf-8')}", flush=True)
            break

        print(f'near end: {row}', flush=True)
        p.sendline(row)
        p.expect("kvm_keys> ")
        print(f"far end: {p.before.decode('utf-8')}", flush=True)
    print('done')

    # look for response from far side
    #p.expect("No more interfaces to dump")
    if remote:
        p.logout()
        
    # wait till timeout
    proc.communicate()

    time.sleep(2) # just to be sure all is cleaned up and it doesn't destablize the os

def server(port = "/dev/serial/by-id/usb-FTDI_FT232R_USB_UART_A50285BI-if00-port0"):
    # this runs on the machine with the usb serial port
    # it expects the input from a remote usbhid-dump
    # it will read usbhid-dump data and parse it
    # and send it out the serial port
    
    # open the serial port
    ser = serial.Serial(port, baudrate=9600, timeout=0.5)


    
    result = {}
    print("starting", flush=True)
    print('Will end upon receiving "No more"', flush=True)
    with fileinput.input(files=None) as f:
        while True:
        #for i in range(50):

            # https://stackoverflow.com/questions/1450393/how-do-you-read-from-stdin
            print('kvm_keys> ', flush=True)
            row = f.readline()
            if 'No more' in row:
                print("timeout detected", flush=True)
                break
            print(row, flush=True)
            if 'STREAM' in row:
                #print('...', flush=True)
                print('kvm_keys> ', flush=True)
                values = f.readline()
                print(values, flush=True)
                values = values.split(' ')
                codes = []
                for v in values[1:]:
                    code = int(v, 16)
                    codes.append(code)
                print(codes, flush=True)
                serial_data = codes_to_hid(codes)
                if codes == [0,0,0x45,0,0,0,0,0]:
                    print('F12 pressed... ending session.', flush=True)
                    break
                #print('.', flush=True)
                ser.write(serial_data)
    print('done', flush=True)
    # wait till timeout
    #proc.communicate()

    

    

def codes_to_hid(codes):
    serial_data = serial.to_bytes(codes)
    return serial_data


if __name__ == '__main__':
    import typer
    typer.run(main)

