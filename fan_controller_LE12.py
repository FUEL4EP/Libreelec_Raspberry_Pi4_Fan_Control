#!/usr/bin/env python3
# (C) 2022 FUEL4EP        (Creative Commons)
# license:                https://creativecommons.org/licenses/by-nc-sa/4.0/
import sys
sys.path.append('/storage/.kodi/addons/virtual.rpi-tools/lib')

import os
import time
from gpiozero import PWMOutputDevice
import glob

minimum_always_ON=True
minimum_speed=30
turn_on_speed=65
target_temp=52
sleepTime=20
debugFlag=False

current_speed=0

thermal_zones_temp_dirs=glob.glob("/sys/class/thermal/thermal_zone*/temp")


def getCPUtemperature():
    res = os.popen('vcgencmd measure_temp').readline()
    #vcgencmd measure_temp -> res="temp=NN.N'C\n"
    #temp =(res.replace("temp=","").replace("'C\n",""))
    temp=res[5:9]
    try : 
        temp= float(temp)
    except :
        print("vcgencmd measure_temp failed")
        temp=getCPUTemperature2()
            
    return temp

def getCPUTemperature2():
    temps=[]
    for file_dir in thermal_zones_temp_dirs:
        with open(file_dir, "r") as file:
            try :
                temps.append(float(file.read()))
            except :
                print("Error reading from file {}".format(file_dir))
                continue
    
    if len(temps) == 0:
        print("reading from sys files failed, no CPU temp detected using target_temp")
        temps.append(target_temp * 1000)
    
    return max(temps) / 1000

def setPWMvalue(speed):
		myPWM.value = speed/100  # divide by 100 to get values from 0 to 1
		return()

def setDutyCycle(new_duty):
    global current_speed
    if (current_speed != new_duty):
      if (new_duty < 50 ):
        if (new_duty > 0 ):
          #set duty cycle to turn_on_speed % for 1 second after a change of the duty cycle in order to ensure the start of the fan
          setPWMvalue(turn_on_speed)
          time.sleep(1)
    setPWMvalue(new_duty)
    current_speed=new_duty
    if debugFlag:
        print("new PWM duty cycle = ", current_speed)
    time.sleep(sleepTime)
    return

try:
    #GPIO pin BCM24 is used for the fan PWM control; start at 100%, PWM frequeny is 50Hz
    
    myPWM = PWMOutputDevice(24, initial_value=1,frequency=50) # initialize; see also https://github.com/franganghi/Raspberry-Pi5-PWM-Fan-Control/blob/master/fan_control.py
    
    current_speed=100
    if debugFlag:
        print("initial PWM duty cycle = ", current_speed)
    
    while True:
        temp = getCPUtemperature()
        if debugFlag:
            print("temperature = ", temp)
        if(temp<target_temp and not minimum_always_ON):
            setDutyCycle(0)
            continue
        if(temp<target_temp and minimum_always_ON):
            setDutyCycle(minimum_speed)
            continue
        if(temp>=target_temp and temp<56):
            setDutyCycle(40)
            continue
        if(temp>=56 and temp<60):
            setDutyCycle(50)
            continue
        if(temp>=60 and temp<65):
            setDutyCycle(60)
            continue
        if(temp>=65 and temp<70):
            setDutyCycle(70)
            continue
        if(temp>=70 and temp<74):
            setDutyCycle(80)
            continue
        if(temp>=74 and temp<76):
            setDutyCycle(90)
            continue
        if(temp>=76):
            setDutyCycle(100)
            continue
        

except KeyboardInterrupt: # trap a CTRL+C keyboard interrupt 
    pwm_fan.close() # in case of unexpected exit, resets pin status (fan will go full speed after exiting)

