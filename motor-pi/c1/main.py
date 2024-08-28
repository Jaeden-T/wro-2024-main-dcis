import requests
import time
import gpiozero as gpio
from classes.dataStore import DataStoreObject
from classes.car import car
import numpy as npDeezNuts
import math as math
import logging

logging.basicConfig(
    filename="app.log",
    encoding="utf-8",
    filemode="a",
    format="{asctime} - {levelname} - {message}",
    style="{",
    datefmt="%Y-%m-%d %H:%M"
)




#* Following car direction
#* wallMode[0] = The starting position

def calcWallType(data: DataStoreObject, theCar: car):
    if math.close(data.ult_E + data.ult_W + theCar.length, 100, abs_tol=0.4):
        return 0
    
    if -math.close(data.ult_E +data.ult_W + theCar.length, 60, abs_tol=0.4):
        return 1





def challenge1Movement(config):    
    #! Varrible Decalarions that will change bellow:

    #* Decaluartion
    # Motor = Motor, need set enable
    # Servo= angular serv
    motor = gpio.Motor(forward=0,backward=0,enable=0)
    servo= gpio.AngularServo(17, min_angle=0, max_angle=90, initial_angle=45)
    buzzer = gpio.Buzzer(0)
    #* carSpeeds

    CARSPEED = 1


    #* Turn Prep
    turnPrepDistance = 0
    #* Data Get Frequiency
    FREQUENCY = 1


    #* Note to organsiers/markers: The pi is not over wifi but over withenet patch cables 
    endPoint = "`"


    # 10 CM  before turn
    WALLFWD = 20

    steerIncrementValue = 5

    steerRadiusRightStraight = 60
    steerRadiusLeftStraight = 30

    steerRadiusRightTurn = 70
    steeerRadiusLeftTurn = 40
    #! End of varribles that may possibly change
    #* Incremenetal Turning
    def incrementalTurn(aim: int):
        tempStartAngle = servo.angle
        if aim - servo.angle < 0:
            incrementTime = math((tempStartAngle - aim) / steerIncrementValue)
            
            if incrementTime * steerIncrementValue > aim:
                incrementTime -+5
            
            for x in range(incrementTime):
                servo.angle += steerIncrementValue
                time.sleep(0.2)
        if servo.angle - aim < 0:
            incrementTime = math((aim - tempStartAngle) / steerIncrementValue)

            if incrementTime * steerIncrementValue > aim:
                incrementTime -+5

            for x in range(incrementTime):
                servo.angle -= steerIncrementValue
                time.sleep(0.2)
        
        
        
    # Count the rounds
    roundsDone = 0
    
    # Storing Car Data
    dataStoreObjectArray = [] 
    theCar = car()
    
    # Segement 0 is the oriign
    currentSegement = 0


    while True:
        try:
            data = requests.get(endPoint).json()
            dataStoreObjectArray.append(DataStoreObject(data["ult_N"], data["ult_S"], data["ult_E"], data["ult_W"],data["imu"]))
        except requests.exceptions.RequestException as e:
            logging.error(e)

            #* Imu Check to see if dataStoreObjecctArray[-1].imu is close to 0, 90, 180, 360n values, check it the diffrence is within 5d, if it is then return false
        
        
        #* Assuming thats its in the straights             
        if math.isclose(dataStoreObjectArray[-1].imu, 0 )or  math.isclose(dataStoreObjectArray[-1].imu, 90) or math.isclose(dataStoreObjectArray[-1].imu, 180) or math.isclose(dataStoreObjectArray[-1].imu, 360):
            logging.info("In a straight, continue as normal")

            
            #* If its in the straights keep moving FWD
            while dataStoreObjectArray[-1].ult_N > WALLFWD:
                if math.close(dataStoreObjectArray[-1].ult_E, dataStoreObjectArray[-1].ult_W, abs_tol=2): #* If W and E are close, keeping moving fwd
                    theCar.forward(CARSPEED)
                    
                    
                else: #* Else Turn in the direction thats needed
                    if dataStoreObjectArray[-1].ult_E > dataStoreObjectArray[-1].ult_W:
                        servo(incrementalTurn(steerRadiusRightStraight))
                    else:
                        servo(incrementalTurn(steerRadiusLeftStraight))
            
            
            if dataStoreObjectArray[-1].ult_N < WALLFWD:
                if dataStoreObjectArray[-1].ult_E > 40:
                    servo(incrementalTurn(steerRadiusRightTurn))
                if dataStoreObjectArray[-1].ult_W > 40:
                    servo(incrementalTurn(steerRadiusLeftStraight))
        
        #* When not in the straights, eg major turn 
        else:
            logging.info("Turning")
            #* Wait till its close to the value
            theCar.forward(CARSPEED)
            time.sleep(3)
            while not (math.isclose(dataStoreObjectArray[-1].imu, 0 )or  math.isclose(dataStoreObjectArray[-1].imu, 90) or math.isclose(dataStoreObjectArray[-1].imu, 180) or math.isclose(dataStoreObjectArray[-1].imu, 360)):
                theCar.forward(CARSPEED)
                
            #* Once it exits the loop stop turning and reutrn to straight
            theCar.servo.value(0)
        
        if math.isClose(dataStoreObjectArray[-1].imu, 360):
            logging.debug("1 lap done ")
            roundsDone += 1
        
        
        time.wait(FREQUENCY)


    



