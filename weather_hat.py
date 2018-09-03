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

PostData = {'TempF': float(), 'DP': float() , 'Humid': float() , 'Pres': float() , 'CPU': float() }
Counter = 0

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
   Atemp = temp -((t_cpu - temp)/5.466)
   DewPointF = get_F(DP)
   CPUF = get_F(t_cpu)
   
   Output = int(RtempF)
   Output = str(Output)
   sense.show_message(Output)

   PostData['TempF'] = PostData['TempF'] + RtempF
   PostData['DP'] = PostData['DP'] + DewPointF
   PostData['Humid'] = PostData['Humid'] + humidity
   PostData['Pres'] = PostData['Pres'] + pressure
   PostData['CPU'] = PostData['CPU'] + CPUF
   Counter = Counter + 1
   
   print(PostCounter)
   if not  ( PostCounter % 60 ):
      avgTemp = PostData['TempF']/Counter
      sendData('Temperature', avgTemp )
      avgDewPointF = PostData['DP']/Counter
      sendData('DewPoint', avgDewPointF )
      avgHumidity = PostData['Humid']/Counter
      sendData('Humidity', avgHumidity)
      avgPressure = PostData['Pres']/Counter
      sendData('Pressure', avgPressure )
      avgCpu = PostData['CPU']/Counter
      sendData('CPU_Temp', avgCpu)
   
      PostCounter = 0
      Counter = 0
      PostData['TempF'] = 0 
      PostData['DP']   = 0
      PostData['Humid'] = 0 
      PostData['Pres'] = 0
      PostData['CPU'] = 0 

   print("==============================")
   time.sleep(WaitTime)
   PostCounter = PostCounter + WaitTime


