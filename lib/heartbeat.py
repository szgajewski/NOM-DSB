#! /usr/bin/python
import RPi.GPIO as GPIO
import time
from threading import Thread

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
led=5
GPIO.setup(led,GPIO.OUT)

class HeartBeat:
 def __init__(self):
  self._running = True

 def terminate(self):
  self._running = False

 def pulse(self):
  try:
   while self._running:
    GPIO.output(led,1)
    time.sleep(0.1)
    GPIO.output(led,0)
    time.sleep(0.1)
    GPIO.output(led,1)
    time.sleep(0.1)
    GPIO.output(led,0)
    time.sleep(4.7)
    #time.sleep(1)
    #print("HB main")
    #return 1
  except KeyboardInterrupt:
   print("\n\nBeat is down")
   return 0

#Create Class
#HB = HeartBeat()
#HB.run()

if __name__ == "__main__":
 print("direct run")
 HeartBeatClass = HeartBeat()
 HeartBeatClass.pulse()

else:
 print("indirect run")
