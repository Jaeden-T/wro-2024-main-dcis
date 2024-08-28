from gpiozero import DistanceSensor


N = DistanceSensor(echo=17, trigger=4)
S = DistanceSensor(echo=17, trigger=4)
E = DistanceSensor(echo=17, trigger=4)
W = DistanceSensor(echo=17, trigger=4)

print("North")
print(N.distance)
print("South")
print(S.distance)
print("East")
print(E.distancce)
print("West")
print(W.distance)
