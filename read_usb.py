# # https://stackoverflow.com/questions/21687867/reading-from-a-usb-keyboard-in-python-with-a-timeout
# import usb.core
# import usb.util
# 
# dev = usb.core.find(idVendor=0x03f0, idProduct=0x034a)
# if dev is None: raise ValueError("Device not found")
# dev.set_configuration()
# endpoint = device[0][(0,0)][0]
# for attempts in xrange(10):
#     try:
#         data = device.read(endpoint.bEndpointAddress, endpoint.wMaxPacketSize)
#     except:
#         data = None
# if data is None: raise RuntimeError("no data found")
# print ('got data', data)

# couldn't get that worknig

# not clear this will work without work
#f = open('/dev/hidraw4', 'rb')
#buffer = f.read(8)
#print('ok')



# https://stackoverflow.com/questions/16175192/command-output-parsing-in-python
import subprocess
import shlex
cmd = "usbhid-dump -m 03f0:034a -es -t 5000"
cmd = shlex.split(cmd)
proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
result = {}
#row = proc.stdout.readline()
#print(row)
#row = proc.stdout.readline().decode("utf-8")
#while True:
for i in range(50):
    row = proc.stdout.readline()
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

# wait till timeout
proc.communicate()
