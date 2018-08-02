#!!aum!!
import RPi.GPIO as GPIO
from gsm_class import gsm
import time
import sys

class main:
    def setup(self):
        print ('Project Init')
        self.GSM = gsm("/dev/ttyUSB0")

        self.GSM.sendCommand("AT")
        print self.GSM.getResponse()
        time.sleep(1)

        if (self.GSM.sendMessage("9029690630", "JTS \n GSM TESTING") == True):
            print 'Message sending Success'
        else:
            print 'Message sending Failed'

    def loop(self):
        print ('Project MainLoop')
        while True:
            time.sleep(1)
            
    def end(self):
        print ('Project End')
        self.GSM.close()


rpi = main()
rpi.setup()
try:
    rpi.loop()
except KeyboardInterrupt:
    rpi.end()
    





