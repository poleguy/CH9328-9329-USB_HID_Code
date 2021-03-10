# kvm_keys
# connect the uart ends into a hub
# connect the hid ends into each machine
# run this program.
# pick the port
# typing F12 is the escape sequence to exit back to the menu
# all keys will be sent to the selected

#sudo python kvm_keys.py --role client --remote debussy.shurelab.com --username dietzn

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
import getpass
import os
import pwd
import queue
import time
import subprocess
import shlex
import os
# See http://pexpect.sourceforge.net/
#import pexpect
#from pexpect import pxssh
import paramiko
from paramiko_expect import SSHClientInteraction


import typer


#@plac.opt('port', "serial port", type=str)
def main(port = "/dev/serial/by-id/usb-FTDI_FT232R_USB_UART_A50285BI-if00-port0",
         hostname = None,
         username = None,
         uid_vid = "03f0:034a",
         timeout = 30000, # msec
         role = "server"):
    # use usbhid to grab keyboard

    PROMPT = '.*]\$\s+'

    print("prepraing connection...")
    
    if "server" in role:
        server(port=port)
        return

    # running locally.
    # grab keyboard

    # must be the client:
    #if "client" in role:
    # https://pexpect.readthedocs.io/en/stable/api/pxssh.html
    #p = pxssh.pxssh()
    #https://github.com/fgimian/paramiko-expect
    p = paramiko.SSHClient()
    
    # Set SSH key parameters to auto accept unknown hosts
    p.load_system_host_keys()
    p.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    # Connect to the host
    p.connect(hostname=hostname, username=username)
    
    #p.force_password = True
    #p.login(hostname, username)

    # Create a client interaction class which will interact with the host
    with SSHClientInteraction(p, timeout=10, display=True) as interact:

        interact.send('source activate')
        interact.expect(PROMPT)
        print(interact.current_output_clean)
        
        interact.send('conda activate ~/CH9328-9329-USB_HID_Code/cenv')
        interact.expect(PROMPT)
        print(interact.current_output_clean)
        cmd = f'python CH9328-9329-USB_HID_Code/kvm_keys.py --port {port}'
        print(cmd)
        interact.send(cmd)
        interact.expect('kvm_keys> ')


        # set up permissions (write access to usb device)
        # https://stackoverflow.com/questions/41238273/execute-shell-command-with-pipes-in-python
        cmd = f"lsusb"
        print(cmd)
        cmd = shlex.split(cmd)
        proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        response = proc.stdout.readlines()
        bus = None
        for line in response:
            line = line.decode('utf-8')
            if uid_vid in line:
                bus = line.split()[1]
                device = line.split()[3][:-1]
                break
     
        if not bus:
            raise ValueError("no bus found. Check --uid-vid is correct with lsusb")
     
        # give read permissions to current user
        user = get_username()
        cmd = f"sudo setfacl -m u:{user}:rw /dev/bus/usb/{bus}/{device}"
        #print(response)
        print(cmd)
        cmd = shlex.split(cmd)
        proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        proc.communicate()
        
        cmd = f"usbhid-dump -m {uid_vid} -es -t {timeout}"
        print(cmd)
        cmd = shlex.split(cmd)
        proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
     
     
        # also open ssh connection
        #cmd = f'ssh dietzn@debussy.shurelab.com "source activate && conda activate ~/CH9328-9329-USB_HID_Code/cenv && echo blah && python3 CH9328-9329-USB_HID_Code/kvm_keys.py"'
        #cmd = shlex.split(cmd)
        #ssh_proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
     
     
        result = {}
        print("ready for input:")

        while True:
        #for i in range(50):
            raw_row = proc.stdout.readline()
            row = raw_row.decode('utf-8').strip('\n')
     
            #print(raw_row)
            if raw_row == b'':            
                print("timeout detected with 'b'",flush=True)
                interact.send('No more')
                interact.expect(PROMPT)
                print(f"far end: {interact.current_output_clean}", flush=True)
                break
     
            if b"00 00 45 00 00 00 00 00" in raw_row:
                print("F12 pressed to exit 'b'",flush=True)
                # eat the F12 so it doesn't get sent
                # and fake out all buttons up to prevent stuck key
                interact.send('00 00 00 00 00 00 00 00')
                interact.expect("kvm_keys> ")
                print(f"far end: {interact.current_output_clean}", flush=True)
                # then end it
                interact.send('No more')
                interact.expect(PROMPT)
                print(f"far end: {interact.current_output_clean}", flush=True)
                interact.send('whoami')
                interact.expect(PROMPT)
                print(f"far end: {interact.current_output_clean}", flush=True)
                break
     
            print(f'near end: {row}', flush=True)
            interact.send(row)
            interact.expect("kvm_keys> ")
            print(f"far end: {interact.current_output_clean}", flush=True)

        print('shutting down...')
     
        # look for response from far side
        #interact.expect("No more interfaces to dump")
        if hostname:
            print("logging out")
            #p.logout()
            # Send the exit command and expect EOF (a closed session)
            interact.send('whoami')
            interact.expect(PROMPT)
            interact.send('exit')
            #interact.expect()
            
        # wait till timeout
        #proc.communicate()
        # can't terminate if it is run with sudo
        proc.terminate()
        proc.wait()
     
        time.sleep(2) # just to be sure all is cleaned up and it doesn't destablize the os
        print('done')

def server(port = "/dev/serial/by-id/usb-FTDI_FT232R_USB_UART_A50285BI-if00-port0"):
    # this runs on the machine with the usb serial port
    # it expects the input from a remote usbhid-dump
    # it will read usbhid-dump data and parse it
    # and send it out the serial port
    
    # open the serial port
    ser = serial.Serial(port, baudrate=9600, timeout=0.5)

    print(port)
    
    result = {}
    print("starting", flush=True)
    print('Will end upon receiving "No more"', flush=True)
    with fileinput.input(files='-') as f:
        while True:
        #for i in range(50):

            # https://stackoverflow.com/questions/1450393/how-do-you-read-from-stdin
            print('kvm_keys> ', flush=True)
            row = f.readline()
            if 'No more' in row:
                # timeout or stopped by client
                print("end of keyboard input detected", flush=True)
                break
            #print(row, flush=True)
            if 'STREAM' in row:
                #print('...', flush=True)
                print('kvm_keys> ', flush=True)
                values = f.readline()
                #print(values, flush=True)
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
                if codes == [0,0,0x44,0,0,0,0,0]:
                    print('F11 pressed... sending 1 byte', flush=True)
                    serial_data =send_bytes(n):
                ser.write(serial_data)
    print('done', flush=True)


    
def test_codes_to_hid():
    a = codes_to_hid([4,0,0,0,0,0,0,0])
    print(a)
    

def send_bytes(ser, n):
    # send dummy bytes in case device gets out of sync. yikes?
    codes = [0] * n
    serial_data = codes_to_hid(codes)    
    return serial_data
    

def codes_to_hid(codes):
    serial_data = serial.to_bytes(codes)
    return serial_data
#https://stackoverflow.com/questions/842059/is-there-a-portable-way-to-get-the-current-username-in-python
def get_username():
    return pwd.getpwuid( os.getuid() )[ 0 ]

if __name__ == '__main__':
    #plac.call(main)
    typer.run(main)

