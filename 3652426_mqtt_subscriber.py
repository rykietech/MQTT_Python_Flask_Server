# tcp client connection

import sqlite3
import sys
import time
from socket import *
import paho.mqtt.client as paho


Broker = "192.168.6.128"
database_name = "3652426_sensorhat_databasemqtt.db"
topic = "test/SensorHatData"
connection = sqlite3.connect(database_name,check_same_thread=False)
cursor = connection.cursor()

   
with connection:
    cursor.execute("DROP TABLE IF EXISTS SENSOR_HAT_data")
    cursor.execute(
        "CREATE TABLE SENSOR_HAT_data (temperature NUMERIC,pressure NUMERIC,humidity NUMERIC,timestamp DATETIME,protocol TEXT)")


def AddSensorHatData(temperature, pressure, humidity,):
    cursor.execute("INSERT INTO SENSOR_HAT_data values ((?),(?),(?),datetime('now'),'mqtt')",
                   (temperature, pressure, humidity))
    connection.commit()



def DisplaySensorHatData():
    connection = sqlite3.connect(database_name)
    cursor = connection.cursor()
    print("Data read from database")
    for data_read in cursor.execute("SELECT * FROM SENSOR_HAT_data"):
        print(data_read)



    # pubsh data from broker 
def on_message(client,userdata,message):
    global message_received
    message_received=str(message.payload.decode("utf-8"))
    temperature,pressure,humidy = [float(i) for i in message.payload.decode("utf-8").split('\n')]
    AddSensorHatData(temperature,pressure,humidy)
    print(message_received)
    
client = paho.Client("client-002")



  
#client.connect(Broker)
client.connect("broker.emqx.io",1883,60) 
client.loop_start()   
client.subscribe(topic)
client.on_message = on_message
print("Subscribing to topic ", "test/SensorHatData")
time.sleep(3000)
client.loop_stop()



