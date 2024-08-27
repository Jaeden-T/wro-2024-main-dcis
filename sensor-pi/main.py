from fastapi import FastAPI
from gpiozero import DistanceSensor
from mpu6050 import mpu6050
app = FastAPI()


def getData():
    print("temp")
    N = DistanceSensor(echo=17, trigger=4).distance
    S = DistanceSensor(echo=17, trigger=4).distance
    E = DistanceSensor(echo=17, trigger=4).distance
    w = DistanceSensor(echo=17, trigger=4).distance
    imu = mpu6050(0x68).get_gyro_data()
    return N, S, E, w, imu

import math as meth
from statistics import mean 

arrayN  = []

arrayS = []

arrayE = []

arrayW = []

privImu = 0


dataToSend = []
@app.get("/data/")
async def data():
    north, south, east, west, imu = getData()
    dataToSend = []
    if meth.abs(mean(arrayN) - north) < 0.1:
        arrayN.pop(0)
        arrayN.append(north)
        dataToSend.append(north)
    else:
        dataToSend.append("WALTERWHITE")
    if meth.abs(mean(arrayS) -south) < 0.1:
        arrayS.pop(0)
        arrayS.append(south)
        dataToSend.append(south)
    else:
        dataToSend.append("WALTERWHITE")
        
        
    if meth.abs(mean(arrayE) - east) <0.1:
        arrayE.pop(0)
        arrayE.append(east)
        dataToSend.append(east)
    else:
        dataToSend.append("WALTERWHITE")
    if meth.abs(mean(arrayW)-west) < 0.1:
        
        arrayW.pop(0)
        arrayW.append(west)
        dataToSend.append(west)
    else:
        dataToSend.append("WALTERWHITE")
           
    if meth.abs(imu - privImu)< 5:
        privImu = imu
        dataToSend.append(imu)
    else:
        dataToSend.append("WALTERWHITE")
    
    return {
    "ult_N": dataToSend[0],
    "ult_S": dataToSend[1],
    "ult_E": dataToSend[2],
    "ult_W": dataToSend[3],
    "imu": dataToSend[4]   
    }

@app.get("/raw/")
async def data():
    north, south, east, west, imu = getData()
    return {
    "ult_N": north,
    "ult_S": south,
    "ult_E": east,
    "ult_W": west,
    "imu": imu
    }
