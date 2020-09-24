import RPi.GPIO as GPIO
import time

servo = 16
GPIO.setmode(GPIO.BCM)
#GPIO.setup(servo,GPIO.OUT)

#p=GPIO.PWM(servo,50)# 50hz frequency
#p.start(0)
# servo -90deg = 10.4 DutyCycle
# servo   0deg =  7.3 DutyCycle
# servo +90deg =  4.2 DutyCycle
# ergo: each degree = 0.0344 (plus or minus to 7.3)
angleConv = 0.03444
#try:
# p.ChangeDutyCycle(10.4)
# print("10.4")
# time.sleep(1)
# p.ChangeDutyCycle(7.3)
# print("7.3")
# time.sleep(1)
# p.ChangeDutyCycle(4.2)
# print("4.2")
# time.sleep(1)

# while True:
#  p.ChangeDutyCycle(8.3)
#  time.sleep(.1)
#  p.ChangeDutyCycle(6.3)
#  time.sleep(.1)

#except KeyboardInterrupt:
# GPIO.cleanup()

def setServoAngle(angle):
 GPIO.setup(servo,GPIO.OUT)
 p = GPIO.PWM(servo,50)
 p.start(0)
 if angle > 90 or angle <-90:
  print("angle out of scope.")
 else:
  value2set = 7.3-(angle*angleConv)
  p.ChangeDutyCycle(value2set)
  time.sleep(0.5)
  print("Servo is settle on %.f degree" % angle)
 return 0

#setServoAngle(-90)
#GPIO.cleanup()
