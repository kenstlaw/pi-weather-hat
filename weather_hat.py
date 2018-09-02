#!/usr/bin/python
import os
import sys
import socket 
import time
import datetime
import time
from sense_hat import SenseHat


sense = SenseHat()
sense.clear()

sense.set_rotation(180)

def get_cpu_temp():
  res = os.popen("vcgencmd measure_temp").readline()
  t = float(res.replace("temp=","").replace("'C\n",""))
  return(t)

def get_F(Ctemp):
   Ftemp = Ctemp * 9.0 / 5.0 + 32
   return(Ftemp)

def sendData(Metric,Value):
   now = str(round(time.time()))
   sock = socket.socket()
   sock.connect( ("localhost", 2003) )
   PrepedValue = int(Value)
   PrepedValue = str(PrepedValue)
   Message = Metric +  " " +  PrepedValue  + " " + now + "\n"
   sock.sendall(Message.encode('utf-8'))
   print(Message.rstrip())
   sock.close() 

Location = 'home'
WaitTime = 5
PostCounter = 0
while True:
   t_cpu = get_cpu_temp()
   ptemp = sense.get_temperature_from_pressure()
   htemp = sense.get_temperature()
   temp = (ptemp + htemp)/2
   Rtemp = temp - ((t_cpu - temp)/1.5)
   Ftemp = get_F(Rtemp)
   RtempF = round(get_F(Rtemp))
   humidity = sense.get_humidity()
   DP = Rtemp - ((100 - humidity)/5)
   pressure = sense.get_pressure()
   #temp_calibrated = temp - ((cpu_temp - temp)/5.466)
   Atemp = temp -((t_cpu - temp)/5.466)
   DewPointF = get_F(DP)
   CPUF = get_F(t_cpu)
   
   Output = int(RtempF)
   Output = str(Output)
   sense.show_message(Output)
   
   print(PostCounter)
   if not  ( PostCounter % 60 ):
      sendData('Temperature',RtempF)
      sendData('DewPoint',DewPointF)
      sendData('Humidity',humidity)
      sendData('Pressure',pressure)
      sendData('CPU_Temp',CPUF)
      PostCounter = 0

   print("==============================")
   time.sleep(WaitTime)
   PostCounter = PostCounter + WaitTime

"""
AtempF = get_F(Atemp)
print("pressure  :", round(pressure))
print("humidity  :", round(humidity))
print("ptemp C   :", round(ptemp))
print("htemp C   :", round(htemp))
print("temp  C   :", round(temp))
print("Rtemp C   :", round(Rtemp))
print("Rtemp F   :", round(RtempF))
print("Avg temp C:", round(temp))
print("Temp  F   :", round(Ftemp))
print("Temp2 F   :", round(AtempF))
print("DewP  F   :", round(DewPointF))
print("CPU temp C:", round(t_cpu))
"""

