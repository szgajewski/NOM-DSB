#!/usr/bin/env python

import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522
import I2C_LCD_driver as LCD
import time

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GND = 22
COLOR = 27
GPIO.setup(GND, GPIO.OUT)
GPIO.setup(COLOR, GPIO.OUT)

class ReaderRFID:
 def readRFID(self):
  GPIO.output(GND,0)
  mylcd = LCD.lcd()
  #mylcd.backlight(0)
  reader = SimpleMFRC522()
  lastID = 0
  lastCheckedTime = time.time()
  repeatNo = 0

  try:
   while True:
    GPIO.output(COLOR,0)
    id, text = reader.read()
    print(id)
    print("since last checked: %.f" % (time.time() - lastCheckedTime))
    #lastCheckedTime = time.time()
    if lastID == id:
     print("even")
     if time.time() - lastCheckedTime > 3:
      repeatNo = 0
     else:
      repeatNo = repeatNo + 1
    else:
     print("odd")
     repeatNo = 0
    print("repeat number: %i" % repeatNo)
    lastCheckedTime = time.time()
    lastID = id
    print(text)
    mylcd.lcd_display_string(text,1)
    GPIO.output(COLOR,1)
    time.sleep(1)
    GPIO.output(COLOR,0)
# check if there is no 3 times in 5 seconds the same card.
# that is an alert signal
    if repeatNo == 2:
     print("Alert! Alert! Alert!")
     repeatNo = 0

  except KeyboardInterrupt:
   print("/n/nBye")

  finally:
   GPIO.cleanup()

if __name__ == "__main__":
 print("direct run")
 readerClass = ReaderRFID()
 readerClass.readRFID()

else:
 print("indirect run")
