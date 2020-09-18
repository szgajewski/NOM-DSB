import RPi.GPIO as GPIO
import time
from threading import Thread
from w1thermsensor import W1ThermSensor
from retrying import retry
from bmp180 import read_bmp180
import analogInputs
#from servoMoto import setServoAngle
from multiprocessing import Process, Pool

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

# RGB leds
RED=25
GPIO.setup(RED,GPIO.OUT)
GREEN=24
GPIO.setup(GREEN,GPIO.OUT)
BLUE=23
GPIO.setup(BLUE,GPIO.OUT)

# RG leds
RG_red = 22
RG_green = 27
GPIO.setup(RG_red, GPIO.OUT)
GPIO.setup(RG_green, GPIO.OUT)

# Yellow led
Y_led = 5
GPIO.setup(Y_led, GPIO.OUT)

# Buzzer
BUZZER=6
GPIO.setup(BUZZER,GPIO.OUT)

# Alarm
alarmPIN = 0
GPIO.setup(alarmPIN, GPIO.OUT)

# Heater
HeaterPIN = 26
GPIO.setup(HeaterPIN, GPIO.OUT)

# FANS
fan1PIN = 13
fan2PIN = 10
GPIO.setup(fan1PIN, GPIO.OUT)
GPIO.setup(fan2PIN, GPIO.OUT)

# buzzers
#bip1PIN = 6
#bip2PIN = 0
#GPIO.setup(bip1PIN, GPIO.OUT)
#GPIO.setup(bip2PIN, GPIO.OUT)

# motors
#ST_motor = 16
DC_motor = 12
#GPIO.setup(ST_motor, GPIO.OUT)
GPIO.setup(DC_motor, GPIO.OUT)

# 1wire therm sensors
# ===
# ID
# 012018c0e6c0 - PT100 waterproof
# 00000964ab6a - DS18B20 soldered
# 3c01b556c86a - DS18D20 naked pins

# Analog Inputs
# 0 - temperature (val*3.3*100/1024)
# 1 - potentiometer (>1000 = 100%, else val/10)
# 2 - PIR (ON/OFF)
# 3 - button (ON/OFF)
# 4 - Door Switch#1
# 5 - Door Switch#2
# 6 - potentiometer#2
# 7 - Light Sensor (<400: DARK, 0%; >1000: LIGHT, 100%)


@retry(stop_max_attempt_number=3, wait_fixed=1000)
def DCmotor(task): # 1 - ON, 0/else - OFF
 report = ""
# motoPIN = 1
# GPIO.setup(motoPIN,GPIO.OUT)
 if task == 1:
  report = "rotate CW"
  GPIO.output(DC_motor,1)
 elif task == 0:
  report = "motor stopped"
  GPIO.output(DC_motor,0)
 else:
  report = "wrong task"
  GPIO.output(DC_motor,0)
 return report

@retry(stop_max_attempt_number=3, wait_fixed=1000)
def get_1wire_temp():
 w1Temp = {}
 for sensor in W1ThermSensor.get_available_sensors():
  w1Temp[sensor] = sensor.get_temperature()
  print("Sensor: %s, temp: %.2f" % (sensor.id, w1Temp[sensor]))
 return w1Temp

@retry(stop_max_attempt_number=3, wait_fixed=1000)
def get_1wire_temp_byID(id):
 temp = round(W1ThermSensor(W1ThermSensor.THERM_SENSOR_DS18B20, id).get_temperature(),2)
 #print("Sensor: %s, temp: %.2f C" % (id, temp))
 return temp

@retry(stop_max_attempt_number=3, wait_fixed=1000)
def analogPotentiometer(inputNo):
 inputVal = analogInputs.analogInput().readAnalogInput(inputNo)
 if inputVal > 1000:
  analogVal = 100
 else:
  analogVal = inputVal/10
 return analogVal

@retry(stop_max_attempt_number=3, wait_fixed=1000)
def analogTemperature(inputNo):
 inputVal = analogInputs.analogInput().readAnalogInput(inputNo)
 analogVal = round(inputVal*3.3/10.24,2) #scale: (val * voltage / resolution)*100
 return analogVal

@retry(stop_max_attempt_number=3, wait_fixed=1000)
def LightSensor(inputNo):
 inputVal = analogInputs.analogInput().readAnalogInput(inputNo)
 if inputVal < 300:
  lightPercentage = 0
 elif inputVal > 1000:
  lightPercentage = 100
 else:
  lightPercentage = round(((inputVal - 300) * 100) / (1000-300),2) # -300: this is minimum value, /500: resolution
 return lightPercentage

#@retry(stop_max_attempt_number=3, wait_fixed=1000)
#def WaterSensor(inputNo):
# inputVal = analogInputs.analogInput().readAnalogInput(inputNo)
# if inputVal < 200:
#  output = "DRY: %s" % inputVal
# elif inputVal < 400:
#  output = "WET: %s" % inputVal
# elif inputVal < 600:
#  output = "LOW LEVEL: %s" % inputVal
# elif inputVal < 850:
#  output = "MID LEVEL: %s" % inputVal
# elif inputVal < 1000:
#  output = "HIGH LEVEL: %s" % inputVal
# else:
#  output = "ALERT! %s" % inputVal
# return output

@retry(stop_max_attempt_number=3, wait_fixed=1000)
def analogDigitalInputs(inputNo):
 inputVal = analogInputs.analogInput().readAnalogInput(inputNo)
 if inputVal > 800:
  digitalVal = 1
 else:
  digitalVal = 0
 return digitalVal

@retry(stop_max_attempt_number=3, wait_fixed=1000)
def heater(status):
 report = ""
 if status == "ON" or status == "on" or status == 1:
  GPIO.output(HeaterPIN, 1)
  report = "Heater is ON."
 elif status == "OFF" or status == "off" or status == 0:
  GPIO.output(HeaterPIN, 0)
  report = "Heater is OFF."
 else:
  GPIO.output(HeaterPIN, 0)
  report = "Wrong operand. Heater is off."
 return report

@retry(stop_max_attempt_number=3, wait_fixed=1000)
def alarmLoud(duration):
# alarmPIN = 0
# GPIO.setup(alarmPIN,GPIO.OUT)
 GPIO.output(alarmPIN,1)
 time.sleep(duration)
 GPIO.output(alarmPIN,0)
 return 0

def bip(duration,rpt,pause):
 iter=0
 try: 
  while rpt>iter:
   GPIO.output(BUZZER,1)
   time.sleep(duration)
   GPIO.output(BUZZER,0)
   time.sleep(pause)
   iter=iter+1
  return True

 except KeyboardInterrupt:
  return 0

def RG_led(status):
 report = ""
 if status == "red" or status == "RED":
  GPIO.output(RG_red,1)
  GPIO.output(RG_green,0)
  report = "RG_LED: RED is ON"
 elif status == "green" or status == "GREEN":
  GPIO.output(RG_red,0)
  GPIO.output(RG_green,1)
  report = "RG_LED: GREEN is ON"
 elif status == "off" or status == "OFF" or status == 0:
  GPIO.output(RG_red,0)
  GPIO.output(RG_green,0)
  report = "RG_LED: RG_LED is OFF"
 else:
  GPIO.output(RG_red,0)
  GPIO.output(RG_green,0)
  report = "RG_LED: Wrong operand. RG_LED is OFF"
 return report

def rgb(_color):
 c_red = 0
 c_green = 0
 c_blue = 0
 if _color == "red" or _color == "RED":
  c_red = 1
 elif _color == "green" or _color == "GREEN":
  c_green = 1
 elif _color == "blue" or _color == "BLUE":
  c_blue = 1
 else:
  pass
 GPIO.output(RED,c_red)
 GPIO.output(GREEN,c_green)
 GPIO.output(BLUE,c_blue)
 return 0

def digitalInputCheck(inBCM):
 GPIO.setup(inBCM.IN)
 inStatus = GPIO.input(inBCM)
 return inStatus

def digitalOutputSet(inBCM,status):
 try:
  GPIO.setup(inBCM,GPIO.OUT)
  GPIO.output(inBCM,status)
  time.sleep(0.1)
  newStatus = GPIO.input(inBCM)
  if newStatus == status:
   print("Status on output %s changed. New status: %s" % (inBCM, newStatus))
  else:
   pirnt("ups.")
 except KeyboardInterrupt:
  print("ups..")
 return newStatus

def digitalOutputSwitch(inBCM):
 newStatus = 0
 try:
  #print("in or out? %s" % GPIO.gpio_function(inBCM))
  GPIO.setmode(GPIO.BCM)
  #GPIO.setup(inBCM,GPIO.IN)
  #checkIOmode = GPIO.gpio_function(inBCM)
  #print("mode: %s" % checkIOmode)
  GPIO.setup(inBCM,GPIO.OUT)
  GPIO.output(inBCM, not GPIO.input(inBCM))
  newStatus = GPIO.input(inBCM) 
 except KeyboardInterrupt:
  print("KI error")
 return newStatus

@retry(stop_max_attempt_number=3, wait_fixed=1000)
def bmp180_temp_pressure():
 bmpTemp, bmpPress = read_bmp180()
 #print("temp: %.2fC, press: %.2f" % (bmpTemp, bmpPress))
 return bmpTemp, bmpPress

@retry(stop_max_attempt_number=3, wait_fixed=1000)
def bmp180_temp():
 bmpTemp, bmpPress = read_bmp180()
 return round(bmpTemp,2)

@retry(stop_max_attempt_number=3, wait_fixed=1000)
def bmp180_pressure():
 bmpTemp, bmpPress = read_bmp180()
 return round(bmpPress,2)

#class ST_MOTOR:
# angle = 0 # degree
# def __init__(self):
#  #self.angle = 90
#  setServoAngle(self.angle)

# def __del__(self):
#  self.angle = 0
#  setServoAngle(0)

# def getAngle(self):
#  return self.angle
#
# def setAngle(self,ang):
#  if ang > 90 or ang < - 90:
#   return self.angle
#  else:
#   self.angle = ang
#   setServoAngle(ang)
#   return self.angle

#mainSTmotor = ST_MOTOR()
#mainSTmotor.setAngle(45)

#@retry(stop_max_attempt_number=5, wait_fixed=1000)
#def allData():
# report = {}
# # inputs
# return report

@retry(stop_max_attempt_number=3, wait_fixed=1000)
def get_PIR_01():
 PIR_01 = {}
 try:
  PIR_01 = { #
   "name": "PIR_01",
   "value":analogDigitalInputs(2),
   "measure_date":time.strftime("%Y-%m-%d %H:%M:%S",time.localtime())}
 except Exception as e:
  print ("PIR_01 Error! Code: {c}, Message: {m}".format(c=type(e).__name__, m=str(e)))
 return PIR_01

@retry(stop_max_attempt_number=3, wait_fixed=1000)
def get_TT_01():
 TT_01 = { #
  "name": "TT_01",
  "value":analogTemperature(0),
  "measure_date":time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())}
 return TT_01

@retry(stop_max_attempt_number=3, wait_fixed=1000)
def get_TT_02():
 TT_02 = { #
  "name": "TT_02",
  "value":get_1wire_temp_byID("012018c0e6c0"),
  "measure_date":time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())}
 return TT_02

@retry(stop_max_attempt_number=3, wait_fixed=1000)
def get_TT_03():
 TT_03 = { #
  "name": "TT_03",
  "value":get_1wire_temp_byID("00000964ab6a"),
  "measure_date":time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())}
 return TT_03

@retry(stop_max_attempt_number=3, wait_fixed=1000)
def get_TT_04():
 TT_04 = { #
  "name": "TT_04",
  "value":get_1wire_temp_byID("3c01b556c86a"),
  "measure_date":time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())}
 return TT_04

@retry(stop_max_attempt_number=3, wait_fixed=1000)
def get_TT_05():
 TT_05 = { #
  "name": "TT_05",
  "value":bmp180_temp(),
  "measure_date":time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())}
 return TT_05

@retry(stop_max_attempt_number=3, wait_fixed=1000)
def get_POT_01():
 POT_01 = { #
  "name": "POT_01",
  "value":analogPotentiometer(1),
  "measure_date":time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())}
 return POT_01

@retry(stop_max_attempt_number=3, wait_fixed=1000)
def get_POT_02():
 POT_02 = { #
  "name": "POT_02",
  "value":analogPotentiometer(6),
  "measure_date":time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())}
 return POT_02

@retry(stop_max_attempt_number=3, wait_fixed=1000)
def get_LS_01():
 LS_01 = { #
  "name": "LS_01",
  "value":LightSensor(7),
  "measure_date":time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())}
 return LS_01

@retry(stop_max_attempt_number=3, wait_fixed=1000)
def get_DS_01():
 DS_01 = { #
  "name": "DS_01",
  "value":analogDigitalInputs(4),
  "measure_date":time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())}
 return DS_01

@retry(stop_max_attempt_number=3, wait_fixed=1000)
def get_DS_02():
 DS_02 = { #
  "name": "DS_02",
  "value":analogDigitalInputs(5),
  "measure_date":time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())}
 return DS_02

@retry(stop_max_attempt_number=3, wait_fixed=1000)
def get_SW_01():
 SW_01 = { #
  "name": "SW_01",
  "value":analogDigitalInputs(3),
  "measure_date":time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())}
 return SW_01

@retry(stop_max_attempt_number=3, wait_fixed=1000)
def get_PT_01():
 PT_01 = { #
  "name": "PT_01",
  "value":bmp180_pressure(),
  "measure_date":time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())}
 return PT_01

 # outputs
@retry(stop_max_attempt_number=3, wait_fixed=1000)
def get_FAN_01():
 if GPIO.input(fan1PIN)==1:
  sValue = "ON"
 else:
  sValue = "OFF"
 FAN_01 = { #
  "name": "FAN_01",
  "value":sValue,
  "measure_date":time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())}
 return FAN_01

@retry(stop_max_attempt_number=3, wait_fixed=1000)
def set_FAN_01(newStatus):
 GPIO.output(fan1PIN,newStatus)
 if GPIO.input(fan1PIN)==1:
  sValue = "ON"
 else:
  sValue = "OFF"
 FAN_01 = {
  "name": "FAN_01",
  "value": sValue,
  "measure_date":time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) }
 return FAN_01

@retry(stop_max_attempt_number=3, wait_fixed=1000)
def get_FAN_02():
 if GPIO.input(fan2PIN)==1:
  sValue = "ON"
 else:
  sValue = "OFF"
 FAN_02 = { #
  "name": "FAN_02",
  "value": sValue,
  "measure_date":time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())}
 return FAN_02

@retry(stop_max_attempt_number=3, wait_fixed=1000)
def set_FAN_02(newStatus):
 GPIO.output(fan2PIN,newStatus)
 if GPIO.input(fan2PIN)==1:
  sValue = "ON"
 else:
  sValue = "OFF"
 FAN_02 = {
  "name": "FAN_02",
  "value": sValue,
  "measure_date":time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())}
 return FAN_02

@retry(stop_max_attempt_number=3, wait_fixed=1000)
def get_BIP_01():
 if GPIO.input(BUZZER)==1:
  sValue = "ON"
 else:
  sValue = "OFF"
 BIP_01 = { #
  "name": "BIP_01",
  "value": sValue,
  "measure_date":time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())}
 return BIP_01

@retry(stop_max_attempt_number=3, wait_fixed=1000)
def set_BIP_01(newStatus):
 GPIO.output(BUZZER,newStatus)
 if GPIO.input(BUZZER)=="1":
  sValue = "ON"
 else:
  sValue = "OFF"
 BIP_01 = {
  "name": "BIP_01",
  "value": sValue,
  "measure_date":time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())}
 return BIP_01

@retry(stop_max_attempt_number=3, wait_fixed=1000)
def get_BIP_02():
 if GPIO.input(alarmPIN)==1:
  sValue = "ON"
 else:
  sValue = "OFF"
 BIP_02 = { #
  "name": "BIP_02",
  "value": sValue,
  "measure_date":time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())}
 return BIP_02

@retry(stop_max_attempt_number=3, wait_fixed=1000)
def set_BIP_02(newStatus):
 GPIO.output(alarmPIN,newStatus)
 if GPIO.input(alarmPIN)==1:
  sValue = "ON"
 else:
  sValue = "OFF"
 BIP_02 = { #
  "name": "BIP_02",
  "value": sValue,
  "measure_date":time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())}
 return BIP_02

@retry(stop_max_attempt_number=3, wait_fixed=1000)
def get_LED_RG():
 if GPIO.input(RG_red)==1:
  sValue = "RED"
 elif GPIO.input(RG_green)==1:
  sValue = "GREEN"
 else:
  sValue = "OFF"
 LED_RG = { #
  "name": "LED_RG",
  "value": sValue,
  "measure_date":time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())}
 return LED_RG

@retry(stop_max_attempt_number=3, wait_fixed=1000)
def set_LED_RG(_color):
 RG_led(_color)
 if GPIO.input(RG_red)==1:
  sValue = "RED"
 elif GPIO.input(RG_green)==1:
  sValue = "GREEN"
 else:
  sValue = "OFF"
 LED_RG = { #
  "name": "LED_RG",
  "value": sValue,
  "measure_date":time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())}
 return LED_RG

@retry(stop_max_attempt_number=3, wait_fixed=1000)
def get_LED_RGB():
 if GPIO.input(RED)==1:
  sValue = "RED"
 elif GPIO.input(GREEN)==1:
  sValue = "GREEN"
 elif GPIO.input(BLUE)==1:
  sValue = "BLUE"
 else:
  sValue = "OFF"
 LED_RGB = { #
  "name": "LED_RGB",
  "value": sValue,
  "measure_date":time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())}
 return LED_RGB

def set_LED_RGB(_color):
 rgb(_color)
 if GPIO.input(RED)==1:
  sValue = "RED"
 elif GPIO.input(GREEN)==1:
  sValue = "GREEN"
 elif GPIO.input(BLUE)==1:
  sValue = "BLUE"
 else:
  sValue = "OFF"
 LED_RGB = { #
  "name": "LED_RGB",
  "value": sValue,
  "measure_date":time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())}
 return LED_RGB

@retry(stop_max_attempt_number=3, wait_fixed=1000)
def get_LED_Y():
 if GPIO.input(Y_led)==1:
  sValue = "YELLOW"
 else:
  sValue = "OFF"
 LED_Y = { #
  "name": "LED_Y",
  "value": sValue,
  "measure_date":time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())}
 return LED_Y

@retry(stop_max_attempt_number=3, wait_fixed=1000)
def set_LED_Y(_status):
 GPIO.output(Y_led,_status)
 if GPIO.input(Y_led)==1:
  sValue = "YELLOW"
 else:
  sValue = "OFF"
 LED_Y = { #
  "name": "LED_Y",
  "value": sValue,
  "measure_date":time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())}
 return LED_Y

#@retry(stop_max_attempt_number=3, wait_fixed=1000)
#def get_ST_MOT():
# ST_MOT = { #
#  "name": "ST_MOT",
#  "value":mainSTmotor.getAngle(),
#  "measure_date":time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())}
# return ST_MOT

#@retry(stop_max_attempt_number=3, wait_fixed=1000)
#def set_ST_MOT(_angle):
# mainSTmotor.setAngle(_angle)
# ST_MOT = { #
#  "name": "ST_MOT",
#  "value":mainSTmotor.getAngle(),
#  "measure_date":time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())}
# return ST_MOT

@retry(stop_max_attempt_number=3, wait_fixed=1000)
def get_DC_MOT():
 if GPIO.input(DC_motor)==1:
  sValue = "ON"
 else:
  sValue = "OFF"
 DC_MOT = { #
  "name": "DC_MOT",
  "value": sValue,
  "measure_date":time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())}
 return DC_MOT

@retry(stop_max_attempt_number=3, wait_fixed=1000)
def set_DC_MOT(_status):
 GPIO.output(DC_motor,_status)
 #DCmotor(_status)
 print("set DC_MOT to : %s" % _status)
 if GPIO.input(DC_motor)==1:
  sValue = "ON"
 else:
  sValue = "OFF"
 DC_MOT = { #
  "name": "DC_MOT",
  "value": sValue,
  "measure_date":time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())}
 return DC_MOT

@retry(stop_max_attempt_number=3, wait_fixed=1000)
def get_HF_01():
 if GPIO.input(HeaterPIN)==1:
  sValue = "ON"
 else:
  sValue = "OFF"
 HF_01 = { #
  "name": "HF_01",
  "value": sValue,
  "measure_date":time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())}
 return HF_01

@retry(stop_max_attempt_number=3, wait_fixed=1000)
def set_HF_01(_status):
 #heater(_status)
 GPIO.output(HeaterPIN,_status)
 if GPIO.input(HeaterPIN)==1:
  sValue = "ON"
 else:
  sValue = "OFF"
 HF_01 = { #
  "name": "HF_01",
  "value": sValue,
  "measure_date":time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())}
 return HF_01

@retry(stop_max_attempt_number=3, wait_fixed=1000)
def getAllData():
 report = []
 report.append(get_PIR_01())
 report.append(get_TT_01())
 report.append(get_TT_02())
 report.append(get_TT_03())
 report.append(get_TT_04())
 report.append(get_TT_05())
 report.append(get_POT_01())
 report.append(get_POT_02())
 report.append(get_LS_01())
 report.append(get_DS_01())
 report.append(get_DS_02())
 report.append(get_SW_01())
 report.append(get_PT_01())
 report.append(get_FAN_01())
 report.append(get_FAN_02())
 report.append(get_BIP_01())
 report.append(get_BIP_02())
 report.append(get_LED_RG())
 report.append(get_LED_RGB())
 report.append(get_LED_Y())
 #report.append(get_ST_MOT())
 report.append(get_DC_MOT())
 report.append(get_HF_01())
 return report

@retry(stop_max_attempt_number=3, wait_fixed=1000)
def getByName(byName):
 func = "get_"+byName
 result = globals()[str(func)]()
 return result

@retry(stop_max_attempt_number=3, wait_fixed=1000)
def setByName(byName,newVal):
 func = "set_"+byName
 if str(newVal).isnumeric():
  result = globals()[str(func)](int(newVal))
 else:
  result = globals()[str(func)](newVal)
 print("Name: %s; new value: %s" % (byName,newVal))
 #print(result)
 return result

@retry(stop_max_attempt_number=3, wait_fixed=1000)
def DecisionSystem(instrument, upLimit, loLimit, regulator, upRule, loRule):
 result = []
 instr = getByName(instrument)
 insValue = instr.get("value")
 regValue = getByName(regulator).get("value")
 result.append(instr)
 if float(insValue) > float(upLimit):
  result.append(setByName(regulator,upRule)) 
 elif float(insValue) < float(loLimit):
  result.append(setByName(regulator,loRule))
 return result