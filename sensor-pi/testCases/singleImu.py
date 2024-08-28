from mpu6050 import mpu6050
imu = mpu6050(0x68).get_gyro_data()
print(imu)