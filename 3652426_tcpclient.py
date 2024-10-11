import sqlite3
import sys
import time
from sense_emu import SenseHat
from socket import *


sense = SenseHat()
HOST = "10.0.0.200"
PORT = 4444
socket_server = socket(AF_INET,SOCK_STREAM)
socket_server.connect((HOST,PORT))
print("Host", HOST, "sending at port: ",PORT)
temp = sense.temperature
press = sense.pressure
humid = sense.humidity

if (temp is not None) and (press is not None) and (humid is not None):
    print('Temperature={0:0.1f}*C Pressure = {1:0.1f} 0mbar Humidity={2:0.1f}%'.format(temp,press,humid))
else:
    print("Failed to get data...")
    time.sleep(2)


def SendData(temp,pressure,humidity):

   
    socket_server.send(str.encode("\n".join([str(temp),str(pressure),str(humidity)])))
   
    
def GetSensorHatData():
    
    temp = sense.temperature
    press = sense.pressure
    humid = sense.humidity
    if (temp is not None) and (press is not None) and (humid is not None):
        print('Temperature={0:0.1f}*C Pressure = {1:0.1f}0mbar Humidity={2:0.1f}%'.format(temp,press,humid))
        temp = round(temp,2)
        press = round(press,2)
        humid = round(humid)
        SendData(temp,press,humid)
    else:
        print("Failed to get data...")
        time.sleep(2)    





def main():
    while True:
        GetSensorHatData()
        time.sleep(0.2)
        


main()
socket_server.close()