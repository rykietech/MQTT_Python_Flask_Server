import sqlite3
import sys
import time
from sense_emu import SenseHat
from socket import *
import paho.mqtt.client as paho

broker = "192.168.6.128" #mosquitto broker address
sense = SenseHat() 
temp = sense.temperature
press = sense.pressure
humid = sense.humidity
client = paho.Client("raspberry-pi")

if (temp is not None) and (press is not None) and (humid is not None):
    print('Temperature={0:0.1f}*C Pressure = {1:0.1f} 0mbar Humidity={2:0.1f}%'.format(temp,press,humid))
else:
    # print if data is not available
    print("Failed to get data...")
    time.sleep(2)
#on message function call
def on_message(client,userdata,message):
    time.sleep(1)
    print(str(message.payload.decode("utf-8")))

# sends the data after subscribe to topic
def SendData(temp,pressure,humidity):

     client.publish("raspberrypi/SensorHatData",str.encode("\n".join([str(temp),str(pressure),str(humidity)])))

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
    client = paho.Client("raspberry-pi")
    client.on_message = on_message
    topic_to_subscribe_to = "raspberrypi/SensorHatData"
    print("Connecting to broker",broker)
    client.loop_start()
    print("Client is subscribing to topic",topic_to_subscribe_to)
    client.subscribe(topic_to_subscribe_to)
    time.sleep(0.2)
    print("Publishing data from sensorhat to topic...")

    while True:
        GetSensorHatData()
        time.sleep(0.2)



main()
client.disconnect()
client.loop_stop()