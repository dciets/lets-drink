import serial
import serial.tools.list_ports
import sys
import struct

ports = serial.tools.list_ports.comports()

if not ports:
    print 'No serial port found'
    sys.exit(1)

port = ports[0].device

ser = serial.Serial(port, 115200)

while True:
    c = ord(ser.read(1))

    if c & 1 == 0:
        button2 = (c >> 1) & 1
        button1 = (c >> 2) & 1
        weight2 = (c >> 4) & 1
        weight1 = (c >> 3) & 1

        print 'input (button1 = %d, button2 = %d, weight1 = %d, weight2 = %d)' % (button1, button2, weight1, weight2)


ser.close()
