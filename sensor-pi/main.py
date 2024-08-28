from fastapi import FastAPI
from gpiozero import DistanceSensor
from mpu6050 import mpu6050
app = FastAPI()

N = DistanceSensor(echo=17, trigger=4)
S = DistanceSensor(echo=17, trigger=4)
E = DistanceSensor(echo=17, trigger=4)
W = DistanceSensor(echo=17, trigger=4)

#* Make Defeintiions to update
def getData():
    print("temp")

    imu = mpu6050(0x68).get_gyro_data()
    return N.distance, S.distance, E. distance, W.distance, imu

def getUlt():
    return N.distance, S.distance, E. distance, W.distance
#* Will be changed afte rtime

class dataStgoreObject():
    def __init__(self):
        self.dataPointOne = 0
        self.dataPointTwo = 0
        
    def cleanData(self ,data: float):
        return ((self.dataPointOne + self.dataPointTwo +data) /3)
    def updateData(self, data:float):
        self.dataPointOne = self.dataPointTwo
        self.dataPointTwo = data




    
def getImuData():
    
    imu = mpu6050(0x68).get_gyro_data()
    
    
import math as meth
from statistics import mean 

#! Call Trackers 
callingImu = 0
callingUlt = 0


dataToSend = []

#! Data Stores
imuStore = dataStgoreObject()


northStore = dataStgoreObject()
southStore = dataStgoreObject()
eastStore = dataStgoreObject()
westStore = dataStgoreObject()

#! End Of Data Stores
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


@pp.get("/test/")
async def test():
    return {"test": 0}
@app.get("/imu/")
async def imu():
    imuDataTemp = getImuData()
    if callingImu < 2:
        if callingImu == 0:
            imuStore.dataPointOne = imuDataTemp
        if callingImu == 1:
            imuStore.dataPointTwo = imuDataTemp
        return {"imu": getImuData()}
    else:
        cleanValue = imuStore.cleanData(imuDataTemp)
        imuStore.updateData(imuDataTemp)
        
    callingImu +=1    
    return {"imu": cleanValue}

@app.get("ult")
async def ult():
    north, south, east, west = getUlt()
    if callingUlt < 2:
        if callingUlt == 0:
            northStore.dataPointOne = north
            southStore.dataPointOne = south
            eastStore.dataPointOne = east
            westStore.dataPointOne = west
        if callingUlt == 1:
            northStore.dataPointTwo = north
            southStore.dataPointTwo = south
            eastStore.dataPointTwo = east
            westStore.dataPointTwo = west
    else:
        cleanNorth = northStore.cleanData(north)
        cleanSouth = southStore.cleanData(south)
        cleanEast = eastStore.cleanData(east)
        cleanWest = westStore.cleanData(west)
        
        northStore.updateData(north)
        westStore.updateData(west)
        eastStore.updateData(east)
        southStore.updateData(south)
        
    
    callingUlt += 1
    return {"ult_N": cleanNorth, "ult_S": cleanSouth, "ult_E": cleanEast, "ult_W": cleanWest}
        
        
    
    
