from fastapi import FastAPI
from gpiozero import DistanceSensor
from mpu6050 import mpu6050
app = FastAPI()
sensor = mpu6050(0x68)
from time import sleep, time
N = DistanceSensor(echo=17, trigger=22)
S = DistanceSensor(echo=16, trigger=24)
E = DistanceSensor(echo=25, trigger=23)
W = DistanceSensor(echo=5, trigger=27)

#* Make Defeintiions to update
def getData():
    print("temp")

    imu = mpu6050(0x68).get_gyro_data()
    return N.distance, S.distance, E. distance, W.distance, imu

def getUlt():
    return N.distance, S.distance, E. distance, W.distance
#* Will be changed afte rtime








# Global variables for storing offsets and angles
gyro_x_offset = 0.0
gyro_y_offset = 0.0
gyro_z_offset = 0.0

angle_x = 0.0
angle_y = 0.0
angle_z = 0.0

last_time = None

def calibrate_gyro(sensor, num_samples=100):
    global gyro_x_offset, gyro_y_offset, gyro_z_offset

    gyro_x_offset = 0.0
    gyro_y_offset = 0.0
    gyro_z_offset = 0.0

    print("Calibrating gyroscope... Please keep the sensor stationary.")
    for _ in range(num_samples):
        gyro_data = sensor.get_gyro_data()
        gyro_x_offset += gyro_data['x']
        gyro_y_offset += gyro_data['y']
        gyro_z_offset += gyro_data['z']
        sleep(0.01)

    gyro_x_offset /= num_samples
    gyro_y_offset /= num_samples
    gyro_z_offset /= num_samples

    # Reset angles after calibration
    global angle_x, angle_y, angle_z
    angle_x = 0.0
    angle_y = 0.0
    angle_z = 0.0

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

@app.get("/calibrate")
async def calibrate():
    calibrate_gyro(sensor)
    return {
        "message": "Gyroscope calibrated successfully.",
        "gyro_x_offset": gyro_x_offset,
        "gyro_y_offset": gyro_y_offset,
        "gyro_z_offset": gyro_z_offset
    }


@app.get("/imuData")
async def imuData():
    global last_time, angle_x, angle_y, angle_z

    if last_time is None:
        last_time = time()

    # Get the current time and calculate the time elapsed
    current_time = time()
    dt = current_time - last_time
    last_time = current_time

    # Get gyroscope data (angular velocity in degrees per second)
    gyro_data = sensor.get_gyro_data()
    gyro_x = gyro_data['x'] - gyro_x_offset
    gyro_y = gyro_data['y'] - gyro_y_offset
    gyro_z = gyro_data['z'] - gyro_z_offset

    # Integrate to get the angle change (angular velocity * time)
    angle_x += gyro_x * dt
    angle_y += gyro_y * dt
    angle_z += gyro_z * dt

    return {
        "x_rotation": round(angle_x, 2),
        "y_rotation": round(angle_y, 2),
        "z_rotation": round(angle_z, 2)
    }

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


@app.get("/test/")
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

@app.get("/ult/")
async def ult():
    north, south, east, west = getUlt()
    global callingUlt
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
        
        
    
    
