#!!AUM!!
import RPi.GPIO as GPIO
import time

# Define some device constants
LCD_WIDTH = 20    # Maximum characters per line
LCD_CHR = True
LCD_CMD = False
LCD_ROW = 4
LCD_COL = 20

LEFT = 1
MID  = 2
RIGHT= 3
LCD_LINE_1 = 0x80 # LCD RAM address for the 1st line
LCD_LINE_2 = 0xC0 # LCD RAM address for the 2nd line
LCD_LINE_3 = 0x94 # LCD RAM address for the 3rd line
LCD_LINE_4 = 0xD4 # LCD RAM address for the 4th line

# Timing constants
E_PULSE = 0.0005
E_DELAY = 0.0005

class LCD_CLASS:
  def __init__(self,rs,en,d4,d5,d6,d7):
    self.rs = rs
    self.en = en
    self.d4 = d4
    self.d5 = d5
    self.d6 = d6
    self.d7 = d7
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    GPIO.setup(self.rs, GPIO.OUT) # RS
    GPIO.setup(en, GPIO.OUT)  # E
    GPIO.setup(d4, GPIO.OUT) # DB4
    GPIO.setup(d5, GPIO.OUT) # DB5
    GPIO.setup(d6, GPIO.OUT) # DB6
    GPIO.setup(d7, GPIO.OUT) # DB7
    # Initialise display
    self.lcd_byte(0x33,LCD_CMD) # 110011 Initialise
    self.lcd_byte(0x32,LCD_CMD) # 110010 Initialise
    self.lcd_byte(0x06,LCD_CMD) # 000110 Cursor move direction
    self.lcd_byte(0x0C,LCD_CMD) # 001100 Display On,Cursor Off, Blink Off
    self.lcd_byte(0x28,LCD_CMD) # 101000 Data length, number of lines, font size
    self.lcd_byte(0x01,LCD_CMD) # 000001 Clear display
    time.sleep(E_DELAY)
  
  def lcd_toggle_enable(self):
    # Toggle enable
    time.sleep(E_DELAY)
    GPIO.output(self.en, True)
    time.sleep(E_PULSE)
    GPIO.output(self.en, False)
    time.sleep(E_DELAY)

  def lcd_byte(self,bits, mode):
    # Send byte to data pins
    # bits = data
    # mode = True  for character
    #        False for command
    GPIO.output(self.rs, mode) # RS
    # High bits
    GPIO.output(self.d4, False)
    GPIO.output(self.d5, False)
    GPIO.output(self.d6, False)
    GPIO.output(self.d7, False)
    if bits&0x10==0x10:
      GPIO.output(self.d4, True)
    if bits&0x20==0x20:
      GPIO.output(self.d5, True)
    if bits&0x40==0x40:
      GPIO.output(self.d6, True)
    if bits&0x80==0x80:
      GPIO.output(self.d7, True)

    # Toggle 'Enable' pin
    self.lcd_toggle_enable()

    # Low bits
    GPIO.output(self.d4, False)
    GPIO.output(self.d5, False)
    GPIO.output(self.d6, False)
    GPIO.output(self.d7, False)
    if bits&0x01==0x01:
      GPIO.output(self.d4, True)
    if bits&0x02==0x02:
      GPIO.output(self.d5, True)
    if bits&0x04==0x04:
      GPIO.output(self.d6, True)
    if bits&0x08==0x08:
      GPIO.output(self.d7, True)

    # Toggle 'Enable' pin
    self.lcd_toggle_enable()


  def lcd_string(self,message,line,style):
    # Send string to display
    # style=1 Left justified
    # style=2 Centred
    # style=3 Right justified
    if style==1:
      message = message.ljust(LCD_WIDTH," ")
    elif style==2:
      message = message.center(LCD_WIDTH," ")
    elif style==3:
      message = message.rjust(LCD_WIDTH," ")

    self.lcd_byte(line, LCD_CMD)

    for i in range(LCD_WIDTH):
      self.lcd_byte(ord(message[i]),LCD_CHR)

  def lcd_str_addr(self,message,row,col):
    if row == 1:
        self.lcd_byte(LCD_LINE_1 + col, LCD_CMD)
    if row == 2:
        self.lcd_byte(LCD_LINE_2 + col, LCD_CMD)
    if row == 3:
        self.lcd_byte(LCD_LINE_3 + col, LCD_CMD)
    if row == 4:
        self.lcd_byte(LCD_LINE_4 + col, LCD_CMD)
    
    for i in range(len(message)):
      self.lcd_byte(ord(message[i]),LCD_CHR)

      
    

if __name__ == '__main__':
    mylcd =  LCD_CLASS(17,27,18,23,24,25)
    mylcd.lcd_string("...Welcome...",LCD_LINE_1,MID)
    time.sleep(2)
    mylcd.lcd_string(" "+str(LCD_COL)+"X"+str(LCD_ROW)+" LCD Init Done ",LCD_LINE_2,MID)
    time.sleep(2)
    mylcd.lcd_string("{}X{}LCD Testing Done".format(LCD_COL,LCD_ROW),LCD_LINE_3,MID)
    time.sleep(2)
    mylcd.lcd_str_addr("Goodbye!!!",4,5)
    GPIO.cleanup()


