import requests
import time
import gpiozero as gpio
from classes.dataStore import DataStoreObject
from classes.car import car
import numpy as npDeezNuts
import math as math
import logging
import cv2
from picamera2 import Picamera2
import numpy as np

#! Modules WRitten
from functions.detection import detectPosition



logging.basicConfig(
    filename="app.log",
    encoding="utf-8",
    filemode="a",
    format="{asctime} - {levelname} - {message}",
    style="{",
    datefmt="%Y-%m-%d %H:%M"
)

#* Configurable 


            
def c2Start():
    
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
        
    
    turn = 0
    while turn != 3:
    picam2 = Picamera2()
    picam2.start_and_capture_file("image.jpg")
    picam2.close()
    # Load the image
    img = cv2.imread('image.jpg')