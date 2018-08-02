#!!aum!!
import RPi.GPIO as GPIO
import time
import sys
import requests


class main:
    def setup(self):
        print ('Project Init')
        time.sleep(1)

    def loop(self):
        print ('Project MainLoop')
        while True:
            payload = {'T': str(23) , 'H': str(50), 'N': str(0), 'L': str(1), 'A':str('E'), 'B': str('E'), 'C': str('E')}
            r = requests.get('https://smartcity672.000webhostapp.com/data.php', params=payload)
            print(r.url)
            time.sleep(5)

            
    def end(self):
        print ('Project Exit')





rpi = main()
rpi.setup()
try:
    rpi.loop()
except KeyboardInterrupt:
    rpi.end()

    





