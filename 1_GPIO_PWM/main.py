#!!AUM!!
#Author: Raviprakash Janu

import RPi.GPIO as GPIO
import time
import sys

OUT_1   = 2
OUT_2   = 3
SWITCH  = 7
HIGH    = GPIO.HIGH
LOW     = GPIO.LOW

class main:
    def setup(self):
        print ('Project Init')
        GPIO.setmode(GPIO.BCM)       # Use BCM GPIO numbers
        GPIO.setwarnings(False)
        
        GPIO.setup(SWITCH, GPIO.IN, pull_up_down = GPIO.PUD_UP)
        GPIO.setup(OUT_1, GPIO.OUT)
        GPIO.setup(OUT_2, GPIO.OUT)
        
        GPIO.output(OUT_1,LOW)
        self.pwm_out = GPIO.PWM(OUT_2,100)
        self.pwm_out.start(0)
        
        time.sleep(1)

    def loop(self):
        print ('Project MainLoop')
        timer = 0
        while True:
            if GPIO.input(SWITCH) == False:
                GPIO.output(OUT_1, HIGH)
            else:
                GPIO.output(OUT_1, LOW)

            self.pwm_out.ChangeDutyCycle(timer)
            
            timer = timer + 1
            if timer > 100:
                timer = 0
            time.sleep(0.1)

            
    def end(self):
        print ('Project End')
        self.pwm_out.stop()
        GPIO.output(OUT_1, LOW)
        GPIO.cleanup()


rpi = main()
rpi.setup()
try:
    rpi.loop()
except KeyboardInterrupt:
    rpi.end()
    





