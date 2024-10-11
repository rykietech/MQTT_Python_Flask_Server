import sqlite3
from asyncio import protocols
from flask import Flask, Response, render_template, request
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import numpy as np
import datetime

# Retrieve data from database
import io

app = Flask(__name__)
def getData(type_ ):
    if type_ == 'mqtt':
        connection = sqlite3.connect('3652426_sensorhat_databasemqtt.db') 
        cursor = connection.cursor() 
        cursor.execute("select * from SENSOR_HAT_data")
        mqtt_rows = cursor.fetchall()
        connection.close()
        return mqtt_rows
    if type_ == 'socket':
        connection = sqlite3.connect('3652426_sensorhat_database.db') 
        cursor = connection.cursor() 
        cursor.execute("select * from SENSOR_HAT_data")
        socket_rows = cursor.fetchall()
        connection.close()
        return socket_rows


def getDataWebSocket():
    conn = sqlite3.connect('3652426_sensorhat_database.db')
    curs = conn.cursor()
    curs.execute("select * from SENSOR_HAT_data")
    rows = curs.fetchall()

 
    for row in curs.execute("SELECT * FROM SENSOR_HAT_data ORDER BY timestamp DESC LIMIT 1"):
        temperature = row[0]
        pressure = row[1]
        humidity = row[2]
        timestamp = row[3]
        protocol = row[4]
      
        return temperature, pressure, humidity,timestamp,protocol,rows
# main route

def getDataMQTT():
    conn = sqlite3.connect('3652426_sensorhat_databasemqtt.db')
    curs = conn.cursor()
    curs.execute("select * from SENSOR_HAT_data")
    rows = curs.fetchall()

    for row in curs.execute("SELECT * FROM SENSOR_HAT_data ORDER BY timestamp DESC LIMIT 1"):
        temperature = row[0]
        pressure = row[1]
        humidity = row[2]
        timestamp = row[3]
        protocol = row[4]
       
    return temperature, pressure, humidity,timestamp,protocol,rows
# main route

@app.route("/")
def index():
    global numSamples
    numSamples = 10

    mqtt_rows = getData('mqtt' )
    socket_rows = getData('socket')
    temperature,pressure,humidity,timestamp,protocol,socket_rows1 = getDataWebSocket()
    templateData = {
        'temperature': temperature,
        'pressure': pressure,
        'humidity': humidity,
        'timestamp':timestamp,
        'protocol': protocol,
        'socket_rows': socket_rows1,
        'socket_rows1': socket_rows,
    }

    temp,pres,humid,times,prot,mqtt_rows1 = getDataMQTT()
    templateDataMQTT = {
        'temperaturemqtt': temp,
        'pressuremqtt': pres,
        'humiditymqtt': humid,
        'timestampmqtt':times,
        'protocolmqtt': prot,
        'mqtt_rows': mqtt_rows1,
        'mqtt_rows1': mqtt_rows,

    }
    return render_template("index.html", **templateData,**templateDataMQTT,)




@app.route('/mqtt_temp.png')
def mqtttemp_png():
    fig = create_figure("mqtt" , 0)
    output = io.BytesIO()
    FigureCanvas(fig).print_png(output)
    return Response(output.getvalue(), mimetype='image/png')

@app.route('/mqtt_hum.png')
def mqtthum_png():
    fig = create_figure("mqtt" , 2)
    output = io.BytesIO()
    FigureCanvas(fig).print_png(output)
    return Response(output.getvalue(), mimetype='image/png')

@app.route('/socket_temp.png')
def sockettemp_png():
    fig = create_figure("socket" , 0)
    output = io.BytesIO()
    FigureCanvas(fig).print_png(output)
    return Response(output.getvalue(), mimetype='image/png')

@app.route('/mqtt_pres.png')
def mqttpres_png():
    fig = create_figure("mqtt" , 1)
    output = io.BytesIO()
    FigureCanvas(fig).print_png(output)
    return Response(output.getvalue(), mimetype='image/png')


@app.route('/socket_pres.png')
def socketpres_png():
    fig = create_figure("socket" , 1)
    output = io.BytesIO()
    FigureCanvas(fig).print_png(output)
    return Response(output.getvalue(), mimetype='image/png')

@app.route('/socket_hum.png')
def sockethum_png():
    fig = create_figure("socket" , 2)
    output = io.BytesIO()
    FigureCanvas(fig).print_png(output)
    return Response(output.getvalue(), mimetype='image/png')



def create_figure(db , type_):
    numSamples = 500
    allData = getData(db)
    allData = np.swapaxes(allData, 0,1)
    dates = allData[3]
    temps = allData[type_].astype(float) # type 0 = temp, 1 = pres , 2 = hum, 3 = dat
    fig = Figure()
    axis = fig.add_subplot(1, 1, 1)
    
    xs = dates
    ys = temps
    axis.plot(xs, ys)
    
    if type_ == 0:
        fig.suptitle(db + " Temperature")
        axis.set_ylabel("Temperature")
    if type_ == 1:
        print(type_)
        fig.suptitle(db + " Pressure")
        axis.set_ylabel("Pressure")
    if type_ == 2:
        axis.set_ylabel("Humidity")
        fig.suptitle(db + " Humidity")
  
    axis.set_xlabel("Date-Time")
    return fig


if __name__ == "__main__":

    app.run(debug=True, port = 5000, host='0.0.0.0')