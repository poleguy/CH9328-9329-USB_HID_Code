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
from pynput import keyboard

def main(port = "/dev/serial/by-id/usb-FTDI_FT232R_USB_UART_A50285BI-if00-port0"):
    # use usbhid to grab keyboard
    ser = serial.Serial(port, baudrate=9600, timeout=0.5)

    #listener = keyboard.Listener(on_press=on_press, suppress=True)
    #listener.start()  # start to listen on a separate thread

    cmd = "usbhid-dump -m 03f0:034a -es -t 5000"
    cmd = shlex.split(cmd)
    proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    result = {}
    #row = proc.stdout.readline()
    #print(row)
    #row = proc.stdout.readline().decode("utf-8")
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
            if codes == 'f12':
                print('F12 pressed... ending session.')
                break
            print('.')
            ser.write(serial_data)
    print('done')
    # wait till timeout
    proc.communicate()

    time.sleep(2) # just to be sure all is cleaned up and it doesn't destablize the os



import subprocess
import shlex




def main_pyinput(port = "/dev/serial/by-id/usb-FTDI_FT232R_USB_UART_A50285BI-if00-port0"):
    ser = serial.Serial(port, baudrate=9600, timeout=0.5)

    listener = keyboard.Listener(on_press=on_press, suppress=True)
    listener.start()  # start to listen on a separate thread
    while True:
        item = q.get()
        print(f'key {item}')
        serial_data = char_to_hid(item)
        if item == 'f12':
            print('F12 pressed... ending session.')
            break
        print('.')
        ser.write(serial_data)
    print('done')
    listener.join()  # remove if main thread is polling self.keys
    print('listener done')
    time.sleep(2) # just to be sure all is cleaned up and it doesn't destablize the os


def char_to_hid(key):
    serial_data = serial.to_bytes([0x00,0x00,0x50,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00])
    return serial_data

def codes_to_hid(codes):
    serial_data = serial.to_bytes(codes)
    return serial_data

# https://stackoverflow.com/questions/11918999/key-listeners-in-python

def on_press(key):
    try:
        k = key.char  # single-char keys
    except:
        k = key.name  # other keys
    #if k in ['1', '2', 'left', 'right']:  # keys of interest
    q.put(k)  # store it in global-like variable
    if key == keyboard.Key.f12:
        return False
    return True
    #print('Key pressed: ' + k)
        #return False  # stop listener; remove this if want more keys


def blah():
    ser = serial.Serial("/dev/serial/by-id/usb-FTDI_FT232R_USB_UART_A50285BI-if00-port0", baudrate=9600, timeout=0.5)
    while True:
        name_str = input('Run CMD:')
        if name_str == 'a':
            # this sends a key down command and then a key up command
            ser.write(serial.to_bytes([0x00,0x00,0x50,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00]))
            print('Left')
        elif name_str == 's':
            ser.write(serial.to_bytes([0x00,0x00,0x51,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00]))
            print('Down')
        elif name_str == 'd':
            ser.write(serial.to_bytes([0x00,0x00,0x4F,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00]))
            print('Right')
        elif name_str == 'w':
            ser.write(serial.to_bytes([0x00,0x00,0x52,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00]))
            print('UP')
        elif name_str == 'e':
            ser.write(serial.to_bytes([0x00,0x00,0x29,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00]))
            print('ESC')
        elif name_str == 'f1':
            ser.write(serial.to_bytes([0x00,0x00,0x3A,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00]))
            print('F1')
        elif name_str == 'f2':
            ser.write(serial.to_bytes([0x00,0x00,0x3B,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00]))
            print('F2')
        elif name_str == 'f3':
            ser.write(serial.to_bytes([0x00,0x00,0x3C,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00]))
            print('F3')
        elif name_str == 'f4':
            ser.write(serial.to_bytes([0x00,0x00,0x3D,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00]))
            print('F4')
        elif name_str == 'f5':
            ser.write(serial.to_bytes([0x00,0x00,0x3E,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00]))
            print('F5')
        elif name_str == 'f6':
            ser.write(serial.to_bytes([0x00,0x00,0x3F,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00]))
            print('F6')
        elif name_str == 'f7':
            ser.write(serial.to_bytes([0x00,0x00,0x40,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00]))
            print('F7')
        elif name_str == 'f8':
            ser.write(serial.to_bytes([0x00,0x00,0x41,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00]))
            print('F8')
        elif name_str == 'f9':
            ser.write(serial.to_bytes([0x00,0x00,0x42,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00]))
            print('F9')
        elif name_str == 'f10':
            ser.write(serial.to_bytes([0x00,0x00,0x43,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00]))
            print('F10')
        elif name_str == 'f11':
            ser.write(serial.to_bytes([0x00,0x00,0x44,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00]))
            print('F11')
        elif name_str == 'f12':
            ser.write(serial.to_bytes([0x00,0x00,0x45,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00]))
            print('F12')
        elif name_str == 't':
            ser.write(serial.to_bytes([0x00,0x00,0x2B,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00]))
            print('tab')
        elif name_str == '+':
            ser.write(serial.to_bytes([0x00,0x00,0x57,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00]))
            print('+')
        elif name_str == '-':
            ser.write(serial.to_bytes([0x00,0x00,0x56,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00]))
            print('-')
        elif name_str == '1':
            ser.write(serial.to_bytes([0x00,0x00,0x1E,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00]))
            print('1')
        elif name_str == '2':
            ser.write(serial.to_bytes([0x00,0x00,0x1F,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00]))
            print('2')
        elif name_str == '3':
            ser.write(serial.to_bytes([0x00,0x00,0x20,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00]))
            print('3')
        elif name_str == '4':
            ser.write(serial.to_bytes([0x00,0x00,0x21,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00]))
            print('4')
        elif name_str == '5':
            ser.write(serial.to_bytes([0x00,0x00,0x22,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00]))
            print('5')
        elif name_str == '6':
            ser.write(serial.to_bytes([0x00,0x00,0x23,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00]))
            print('6')
        elif name_str == '7':
            ser.write(serial.to_bytes([0x00,0x00,0x24,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00]))
            print('7')
        elif name_str == '8':
            ser.write(serial.to_bytes([0x00,0x00,0x25,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00]))
            print('8')
        elif name_str == '9':
            ser.write(serial.to_bytes([0x00,0x00,0x26,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00]))
            print('9')
        elif name_str == '0':
            ser.write(serial.to_bytes([0x00,0x00,0x27,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00]))
            print('0')
        else:
            print('N/A')



if __name__ == '__main__':
    q = queue.Queue()
    main()

