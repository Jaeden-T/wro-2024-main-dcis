from gpiozero import DistanceSensor


N = DistanceSensor(echo=2, trigger=17)

print("North")
print(N.distance)

