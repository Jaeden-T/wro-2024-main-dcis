from gpiozero import Button

button = Button(26)
mode = Button(2)
button.wait_for_press()


if mode == True:
    print("MODE 1 (CHALLEGNE 1)")
if mode == False:
    print("MODE 2 (CHALLENGE2)")