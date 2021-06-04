# CH9328-USB_HID_Code

This code must be run on a machine with a physical keyboard connected via usb. It has not been tested on laptop keyboards and might lock up the keyboard requiriing a reboot. Plug and unplug the keyboard if it stops responding.

The machine with the physical machine is called the client. It talks to a server via ssh. In this example the server is debussy.shurelab.com. The server must be preconfigured with this repo checked out in the home directary and init.sh sourced to set up the environment.

The server sends serial commands to the HID device which is plugged into your target machine.
There is also an HDMI to USB Video Capture card connected from the target machine back to debussy. This can be viewed by running:

vlc 

and opening the device with a name like /dev/video0

run:

git clone https://github.com/poleguy/CH9328-9329-USB_HID_Code.git

cd CH9328-9329-USB_HID_Code

to set up the first time:

source ./init.sh

to use: 

determine uid-vid of your local keyboard:

--uid-vid

should be found by plugging in a usb keyboard and checking

lsusb

enter ssh target for --userame and --hostname

python kvm_keys.py --port /dev/serial/by-id/usb-1a86_USB_Serial-if00-port0 --role client --username dietzn --hostname debussy.shurelab.com --uid-vid 03f0:064a

--port can be found (on remote machine) by plugging in usb and looking in

ls /dev/serial/by-id

or 

ls /dev/serial/by-path


to test on your own local machine:

python kvm_keys.py --port /dev/serial/by-path/pci-0000\:00\:14.0-usb-0\:1\:1.0-port0 --role client --username poleguy --hostname localhost --uid-vid 17ef:6099
