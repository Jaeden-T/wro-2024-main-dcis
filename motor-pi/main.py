from gpiozero import Button
import requests
from c1.main import challenge1Movement
calibrate = requests.get("http://pi3Sense.local:8000/calibrate")
print(calibrate)
import gpiozero as gpio

servo= gpio.AngularServo(27, min_angle=0, max_angle=90, initial_angle=45)

button = Button(26)
mode = Button(22)

servo.angle = 45
servo.angle = 70
servo.angle = 20
servo.angle = 45

button.wait_for_press()
print("Button pressed")
if mode.is_pressed== True:
    print("MODE 1 (CHALLEGNE 1)")
    challenge1Movement(servo)
if mode.is_pressed == False:
    print("MODE 2 (CHALLENGE2)")