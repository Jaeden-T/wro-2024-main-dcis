from gpiozero import Button

from c1.main import challenge1Movement

button = Button(26)
mode = Button(22)

button.wait_for_press()
print("Button pressed")
if mode.is_pressed== True:
    print("MODE 1 (CHALLEGNE 1)")
    challenge1Movement()
if mode.is_pressed == False:
    print("MODE 2 (CHALLENGE2)")