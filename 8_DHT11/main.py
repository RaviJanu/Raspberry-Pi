#!!aum!!
import RPi.GPIO as GPIO
import time
from dht11 import DHT11

DHT  = 4

class main:
    def setup(self):
        GPIO.setmode(GPIO.BCM)       # Use BCM GPIO numbers
        GPIO.setwarnings(False)
        self.dht = DHT11(DHT)
        print ('Project Init')
        time.sleep(1)

    def loop(self):
        print ('Project MainLoop')
        while True:
            result = self.dht.read()
            if result.is_valid():
                temperature = result.temperature
                humidity    = result.humidity
                print("Temperature: "+str(temperature)+" C")
                print("Humidity: "+str(humidity)+" %")
            else:
                print("DHT ERROR")

            time.sleep(1)
            
    def end(self):
        print("Exit file")
        GPIO.cleanup()





rpi = main()
rpi.setup()
try:
    rpi.loop()
except KeyboardInterrupt:
    rpi.end()





