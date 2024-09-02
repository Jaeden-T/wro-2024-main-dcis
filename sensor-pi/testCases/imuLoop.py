from mpu6050 import mpu6050
from time import sleep
while True:
	imu = mpu6050(0x68).get_gyro_data()

	print(imu)
	sleep(5)
