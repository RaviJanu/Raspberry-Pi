#!!AUM!!
import RPi.GPIO as GPIO
import time
from lcd import LCD_CLASS

LCD_ROW = 4
LCD_COL = 20
LEFT = 1
MID  = 2
RIGHT= 3
LCD_LINE_1 = 0x80 # LCD RAM address for the 1st line
LCD_LINE_2 = 0xC0 # LCD RAM address for the 2nd line
LCD_LINE_3 = 0x94 # LCD RAM address for the 3rd line
LCD_LINE_4 = 0xD4 # LCD RAM address for the 4th line
mylcd =  LCD_CLASS(17,27,18,23,24,25)


class main:
    def setup(self):
        print ('Project Init')
        time.sleep(1)

    def loop(self):
        print ('Project MainLoop')
        mylcd.lcd_string("...Welcome...",LCD_LINE_1,MID)
        time.sleep(2)
        mylcd.lcd_string(" "+str(LCD_COL)+"X"+str(LCD_ROW)+" LCD Init Done ",LCD_LINE_2,MID)
        time.sleep(2)
        mylcd.lcd_string("{}X{}LCD Testing Done".format(LCD_COL,LCD_ROW),LCD_LINE_3,MID)
        time.sleep(2)
        mylcd.lcd_str_addr("Goodbye!!!",4,5)

            
    def end(self):
        GPIO.cleanup()






rpi = main()
rpi.setup()
rpi.loop()
rpi.end()
    





