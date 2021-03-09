# CH9328-USB_HID_Code

run:

to set up the first time:

./init.sh

to test on your own local machine:

python kvm_keys.py --port /dev/serial/by-path/pci-0000\:00\:14.0-usb-0\:1\:1.0-port0 --role client --username poleguy --remote localhost --uid-vid 17ef:6099

to use: 

enter ssh target for --userame and --remote

--uid-vid
should be found by plugging in a usb keyboard and checking
lsusb

--port can be found by plugging in usb and looking in
ls /dev/serial/by-id
or 
ls /dev/serial/by-path


