import serial
import serial.tools.list_ports
import sys

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
        print 'input message (button1 = %d, button2 = %d)' % (button1, button2)
    else:
        print 'weight message'

ser.close()
