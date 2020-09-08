import I2C_LCD_driver as LCD
import time
from w1thermsensor import W1ThermSensor
from gpiozero import Button
import RPi.GPIO as GPIO
import rfid_read
from retrying import retry

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
led=5
buzzer=6
fan=13
GPIO.setup(led,GPIO.OUT)
GPIO.setup(buzzer,GPIO.OUT)
GPIO.setup(fan,GPIO.OUT)

mylcd = LCD.lcd()
#mylcd.backlight(0)
mylcd.lcd_display_string("God is good!",1)
mylcd.lcd_display_string("~All the time!",2,2)
#mylcd.lcd_clear()

milliseconds = 100
repeated = 1
pause = 100

#readerRFID = rfid_read.ReaderRFID()
#readerRFID.readRFID()

def bip(milliseconds, repeated, pause):
 iter = 0
 while iter < repeated:
  GPIO.output(buzzer,1)
  time.sleep(milliseconds/1000)
  GPIO.output(buzzer,0)
  time.sleep(pause/1000)
  iter = iter + 1

@retry(stop_max_attempt_number=3, wait_fixed=1000)
def get_1wire_temp():
 w1Temp = {}
 for sensor in W1ThermSensor.get_available_sensors():
  w1Temp[sensor] = sensor.get_temperature()
 return w1Temp

@retry(stop_max_attempt_number=3, wait_fixed=1000)
def get_1wire_temp_byID(ID):
 w1Temp = 0
 sensorRasPi = W1ThermSensor(W1ThermSensor.THERM_SENSOR_DS18B20, ID)
 tempRasPi = sensorRasPi.get_temperature()
 return tempRasPi

try:
 while True:
  try:
   for sensor in get_1wire_temp():
    print("Sensor %s has temperature %.2f" % (sensor.id, sensor.get_temperature()))
   #sensorRasPi = W1ThermSensor(W1ThermSensor.THERM_SENSOR_DS18B20, "00000964ab6a")
   #tempRasPi = sensorRasPi.get_temperature()
   tempRasPi = get_1wire_temp_byID("00000964ab6a")
   strTempRasPi = ("RPi temp: %.2fC" % tempRasPi)
   print (strTempRasPi)
   try:
    mylcd.lcd_display_string(strTempRasPi,2)
   except KeyboardInterrput:
    print("")
   if tempRasPi>29:
    bip(100,1,0)
    GPIO.output(fan,1)
   elif tempRasPi<28:
    GPIO.output(fan,0)
    bip(100,2,100)
   else:
    time.sleep(0)
    #bip(100,3,100)
   time.sleep(10)
  except KeyboardInterrupt:
   print("/n/nbye!")

except KeyboardInterrupt:
    print("\nGod still in control.")
    GPIO.cleanup()
