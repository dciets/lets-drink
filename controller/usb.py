from controller import *
import sys
import serial
import struct
import serial.tools.list_ports
import time


class USB(Controller):
    EVENT_TYPES = [Controller.BUTTON_RELEASED, Controller.BUTTON_PRESSED]

    def __init__(self):
        ports = serial.tools.list_ports.comports()

        if not ports:
            print 'No serial port found'
            sys.exit(1)

        self.port = ports[0].device

        self.device = serial.Serial(self.port, 115200, timeout=0)
        self.button1 = 0
        self.button2 = 0
        self.weight1 = 0
        self.weight2 = 0

        Controller.__init__(self)

    def read(self):

        for event in pygame.event.get(pygame.QUIT):
            pygame.quit()
            sys.exit(0)

        for event in pygame.event.get(pygame.KEYDOWN):
            if event.key == pygame.K_q:
                pygame.quit()
                sys.exit(0)

        c = self.device.read(1)

        if c:
            c = ord(c)
        else:
            return

        if c & 1 == 0:
            button2 = (c >> 1) & 1
            button1 = (c >> 2) & 1
            weight2 = (c >> 4) & 1
            weight1 = (c >> 3) & 1

            if button1 != self.button1:
                self.button1 = button1
                pygame.event.post(pygame.event.Event(USB.EVENT_TYPES[button1], index=0))

            if button2 != self.button2:
                self.button2 = button2
                pygame.event.post(pygame.event.Event(USB.EVENT_TYPES[button2], index=1))

            if weight1 != self.weight1:
                self.weight1 = weight1
                pygame.event.post(pygame.event.Event(USB.EVENT_TYPES[weight1], index=2))

            if weight2 != self.weight2:
                self.weight2 = weight2
                pygame.event.post(pygame.event.Event(USB.EVENT_TYPES[weight2], index=3))
