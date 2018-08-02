#!!aum!!
import RPi.GPIO as GPIO
from FingerPrint import fp_class
import time
import sys

class main:
    def setup(self):
        print ('Project Init')
        self.fp = fp_class('/dev/ttyUSB0')
        self.fp.enrollNgetID()
        time.sleep(1)

    def loop(self):
        print ('Project MainLoop')
        while True:
            self.fp.CheckFingerPrint()
            time.sleep(1)
            
    def end(self):
        print ('Project End')


rpi = main()
rpi.setup()
try:
    rpi.loop()
except KeyboardInterrupt:
    rpi.end()
    





