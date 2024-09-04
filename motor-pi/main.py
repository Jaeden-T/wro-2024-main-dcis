from gpiozero import Button

from c1.main import challenge1Movement

button = Button(26)
mode = Button(2)

button.wait_for_press()
print("Button pressed")
if mode == True:
    print("MODE 1 (CHALLEGNE 1)")
    challenge1Movement()
if mode == False:
    print("MODE 2 (CHALLENGE2)")