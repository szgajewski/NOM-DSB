import RPi.GPIO as GPIO
import time
from threading import Thread
import heartbeat
#import w1Therm
from multiprocessing import Process
import sys
import rfid_write
import rfid_read
import lib_NOM as LIB

degree_sign = u'\N{DEGREE SIGN}'
step_motor_angle = 90


def func1():
    print("start func1")
    LIB.bip(0.1,3,0.5)
  #  rfid_read.ReaderRFID().readRFID()
    LIB.setServoAngle(-90)
    print(LIB.DCmotor(1))
    time.sleep(1)
    print(LIB.DCmotor(0))
    print("end func1")

def func2():
    print ("start func2")
    print("temp is: %.2f" % LIB.get_1wire_temp_byID("00000964ab6a")) #DS18B20 soldered
    LIB.rgb(1,0,0)
    time.sleep(0.5)
    LIB.rgb(0,1,0)
    time.sleep(0.5)
    LIB.rgb(0,0,1)
    time.sleep(0.5)
    LIB.rgb(0,0,0)
    print("Potentiometer_1 value: %.1f%% | Potentiometer_2 value: %.1f%%" % (LIB.analogPotentiometer(1), LIB.analogPotentiometer(6)))
    print("Analog thermometer value: %.2f%sC" % (LIB.analogTemperature(0), degree_sign))
    print("Digital status of analog input. Door Switch_1: %s | Door Switch_2: %s" % (LIB.analogDigitalInputs(4),LIB.analogDigitalInputs(5)))
    print("Light sensor status: %.2f%%" % LIB.LightSensor(7))
    print ("end func2")

def func3():
 print("start func3")
 #print("Turn fan on.")
 #check = LIB.digitalOutputSet(26,0)
 #changeStatus = LIB.digitalOutputSwitch(26)
 #time.sleep(1)
 changeStatus = LIB.digitalOutputSwitch(5)
 print("button status: %s" % LIB.analogDigitalInputs(3))
 #LIB.digitalOutputSet(17,1)
# print("turn heater ON")
 print("New output (#5) status: %s" % changeStatus)
 #heartbeat.HeartBeat().pulse()
 print(LIB.heater(0))
 print("end func3")

def func4():
 print("start func4")
# bmpTemp, bmpPressure = LIB.bmp180_temp_pressure()
# print("BMP180. Temperature: %.2f%sC. Pressure: %.2fhPa" % (bmpTemp, degree_sign, bmpPressure))
# LIB.alarmLoud(0.1)
# print(LIB.RG_led("red"))
# time.sleep(0.5)
# print(LIB.RG_led("green"))
# time.sleep(1)
# print(LIB.RG_led(0))
# print(LIB.allData())
 print(LIB.getAllData(step_motor_angle))
 print("end func4")

if __name__=='__main__':
#    p1 = Process(target = func1)
#    p1.start()
#    p2 = Process(target = func2)
#    p2.start()
#    p3 = Process(target = func3)
#    p3.start()
    p4 = Process(target = func4)
    p4.start()
