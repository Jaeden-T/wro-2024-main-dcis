#$ Loader
import gpiozero as gpio
#* import C1 and C2 Here
import C2.main as challenge2
import C1.main as challenge1


#* Button
REPLACE = 0
b = gpio.Button(REPLACE)
c1 = gpio.button(REPLACE)
c2 = gpio.button(REPLACE)
b.wait_for_press()

if c1.is_pressed == True:
    challenge1()
if c2.is_pressed == True:
    challenge2()
else:
    print("Error")