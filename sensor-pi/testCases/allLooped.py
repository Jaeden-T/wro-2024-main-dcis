from mpu6050 import mpu6050
from gpiozero import DistanceSensor

N = DistanceSensor(echo=17, trigger=4)
S = DistanceSensor(echo=17, trigger=4)
E = DistanceSensor(echo=17, trigger=4)
W = DistanceSensor(echo=17, trigger=4)


imu = mpu6050(0x68).get_gyro_data()

while True:
    print("North")
    print(N.distance)
    print("South")
    print(S.distance)
    print("East")
    print(E.distancce)
    print("West")
    print(W.distance)

    print("IMU")
    print(imu)