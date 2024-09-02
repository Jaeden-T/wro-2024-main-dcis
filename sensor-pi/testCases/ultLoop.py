

from gpiozero import DistanceSensor
from time import sleep
front  = DistanceSensor(echo=17, trigger=22)
back = DistanceSensor(echo=16, trigger=24)
left = DistanceSensor(echo=5, trigger=27)
right  = DistanceSensor(echo=25, trigger=23)



while True:
    print("front  ")
    print(front.distance *100)
    print("Back")
    print(back.distance*100)
    print("Left")
    print(left.distance*100)
    print("Right")
    print(right.distance*100)
    print("\n")
    sleep(1)

