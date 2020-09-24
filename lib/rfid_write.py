#!/usr/bin/env python

import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522

reader = SimpleMFRC522()

def rfid_write():
 try:
  text = input("New data:")
  print("Now place your tag to write")
  reader.write(text)
  print("Written. New text is: %s" % text)

 finally:
  GPIO.cleanup()
