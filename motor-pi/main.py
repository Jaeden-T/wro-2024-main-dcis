from gpiozero import Button
import requests
from c1.main import challenge1Movement
calibrate = requests.get("http://pi3Sense.local:8000/calibrate")
print(calibrate)
button = Button(26)
mode = Button(22)

button.wait_for_press()
print("Button pressed")
if mode.is_pressed== True:
    print("MODE 1 (CHALLEGNE 1)")
    challenge1Movement()
if mode.is_pressed == False:
    print("MODE 2 (CHALLENGE2)")