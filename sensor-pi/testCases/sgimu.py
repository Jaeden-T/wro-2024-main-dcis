from mpu6050 import mpu6050
from time import sleep, time
import csv

# Initialize the sensor
sensor = mpu6050(0x68)

# Function to calibrate the gyroscope
def calibrate_gyro(sensor, num_samples=1009):
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

    return gyro_x_offset, gyro_y_offset, gyro_z_offset

# Calibrate the gyroscope
gyro_x_offset, gyro_y_offset, gyro_z_offset = calibrate_gyro(sensor)

# Initialize variables for cumulative angles
angle_x = 0.0
angle_y = 0.0
angle_z = 0.0

# Get the initial time
last_time = time()

# Open a CSV file for writing
with open('gyro_data.csv', 'w', newline='') as csvfile:
    csvwriter = csv.writer(csvfile)

    while True:
        # Get the current time and calculate the time elapsed
        current_time = time()
        dt = current_time - last_time
        last_time = current_time

        # Get gyroscope data (angular velocity in degrees per second
        try:
            gyro_data = sensor.get_gyro_data()
        except OSError as e:
            print(f"Encountered an I/O error: {e}. Retrying...")
            time.sleep(0.1)  # small delay before retry
            gyro_data = sensor.get_gyro_data()  # retry reading

        gyro_x = gyro_data['x'] - gyro_x_offset
        gyro_y = gyro_data['y'] - gyro_y_offset
        gyro_z = gyro_data['z'] - gyro_z_offset

        # Integrate to get the angle change (angular velocity * time)
        angle_x += gyro_x * dt
        angle_y += gyro_y * dt
        angle_z += gyro_z * dt

        # Write the cumulative rotation angles to the CSV file
        csvwriter.writerow([angle_x, angle_y, angle_z])

        # Print the cumulative rotation angles
        print(f"X Rotation: {angle_x:.2f}°, Y Rotation: {angle_y:.2f}°, Z Rotation: {angle_z:.2f}°")

        # Sleep to give time for the next reading
        sleep(0.1)  # Adjust the sleep time as needed



