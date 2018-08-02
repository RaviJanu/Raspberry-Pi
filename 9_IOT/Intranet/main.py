#!!aum!!
import RPi.GPIO as GPIO
import time
from SOCKET import socket_class
import sys



class main:
    def setup(self):
        print ('Project Init')
        self.iot = socket_class()
        self.iot.setupServer('192.168.0.109',1234)
        self.iot.setupConnection()
        time.sleep(1)

    def loop(self):
        print ('Project MainLoop')
        while True:
            self.iot.send_data_conn("hello world_")
            time.sleep(5)

            
    def end(self):
        self.iot.close_connection()
        print ('Project Exit')





rpi = main()
rpi.setup()
try:
    rpi.loop()
except KeyboardInterrupt:
    rpi.end()

    





