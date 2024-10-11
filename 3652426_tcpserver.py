# tcp client connection

import sqlite3
import sys
import time
from socket import *

HOST = ""
#HOST = "192.168.6.128"
PORT = 4444

database_name = "3652426_sensorhat_database.db"
connection = sqlite3.connect(database_name)
cursor = connection.cursor()
client_socket = socket(AF_INET, SOCK_STREAM)
# tcp
# sqlite3 connection creates database    
with connection:
    cursor.execute("DROP TABLE IF EXISTS SENSOR_HAT_data")
    cursor.execute(
        "CREATE TABLE SENSOR_HAT_data (temperature NUMERIC,pressure NUMERIC,humidity NUMERIC,timestamp DATETIME,protocol TEXT)")

#takes temperature pressure and humifity and adds it into the database
def AddSensorHatData(temperature, pressure, humidity,):
    cursor.execute("INSERT INTO SENSOR_HAT_data values ((?),(?),(?),datetime('now'),'tcp')",
                   (temperature, pressure, humidity))
    connection.commit()


#selects the data from sql and prints the data in the terminal
def DisplaySensorHatData():
    connection = sqlite3.connect(database_name)
    cursor = connection.cursor()
    print("Data read from database")
    for data_read in cursor.execute("SELECT * FROM SENSOR_HAT_data"):
        print(data_read)


   
   
   

def main():
    #main function for socket programming
  
    client_socket.bind((HOST,PORT))
    client_socket.listen(1)
    connect,addr = client_socket.accept()
    while True:
        temperature,pressure,humidy = [float(i) for i in connect.recv(2048).decode('utf8').split('\n')]
        print("Temperature",temperature)
        AddSensorHatData(temperature,pressure,humidy) # calls AddSensorHatData function
        DisplaySensorHatData() # calls DisplaySensorHatData function
  

#runs main function
main()
client_socket.close()    
connection.close()