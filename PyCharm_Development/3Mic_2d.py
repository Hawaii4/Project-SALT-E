import math as math
import matplotlib.pyplot as plt

#reference sensor set as sensor1

class Sensor:
    def __init__(self):
        self.coords = [0,0]

    def setcoords(self, x, y):
        self.coords = [x,y]

    def getdist(self, comparecoords):
        dist = (comparecoords[0] - self.coords[0])**2 + (comparecoords[1] - self.coords[1])**2
        return math.sqrt(dist)

    def m(self):
        m = 0.5*(self.getdist([0,0])**2 - s1.getdist([0,0])**2 - s1.getdist(self.coords)**2)
        return m

s1 = Sensor()
s1.setcoords(2,1)

s2 = Sensor()
s2.setcoords(3,3)

s3 = Sensor()
s3.setcoords(1,4)

alpha = (s1.getdist(s2.coords)*(s3.coords[0]-s1.coords[0]) - s1.getdist(s3.coords)*(s2.coords[0]-s1.coords[0]))/(-s1.getdist(s2.coords)*(s3.coords[1]-s1.coords[1])+s1.getdist(s3.coords)*(s2.coords[1]-s1.coords[1]))
beta = (s1.getdist(s3.coords)*s1.m()-s1.getdist(s2.coords)*s2.m())/(-s1.getdist(s2.coords)*(s3.coords[1]-s1.coords[1])-s1.getdist(s3.coords)*(s2.coords[1]-s1.coords[1]))

print("alpha = ", alpha)
print("beta = ", beta)

a = ((1+alpha**2)-((s2.coords[0] - s1.coords[0]) + (s2.coords[1] - s1.coords[1])*alpha)**2) / (s1.getdist(s2.coords)**2)
b = -2*((s1.coords[0] + (s1.coords[1] - beta)*alpha) - ((s2.coords[0] - s1.coords[0]) + (s2.coords[1] - s1.coords[1])*alpha)*((s2.coords[1] - s1.coords[1])*beta - s1.m()))
c = (s1.coords[1] - beta)**2 + s1.coords[0]**2 - (((s2.coords[1] - s1.coords[1])*beta - s1.m()) / (s1.getdist(s2.coords)**2))**2

print(a)
print(b)
print(c)

xs1 = (-b + math.sqrt(b**2 - 4*a*c))/(2*a)
xs2 = (-b - math.sqrt(b**2 - 4*a*c))/(2*a)
ys1 = alpha*xs1 + beta
ys2 = alpha*xs2 + beta

print(xs1)
print(xs2)
print(ys1)
print(ys2)

plt.figure(figsize=(10,10))
plt.plot(s1.coords[0], s1.coords[1], 'o', color='red')
plt.plot(s2.coords[0], s2.coords[1], 'x', color='blue')
plt.plot(s3.coords[0], s3.coords[1], 'x', color='blue')
plt.plot(xs1, ys1, 'o', color='green')
plt.plot(xs2, ys2, 'o', color='green')
plt.grid(True)
plt.show()
plt.close()


## why can't the sound come from the other side?
## this program is for fixed coordinates of the sensors -> don't understand why it can only be those two points
## program 3Mic_2d_dot.py for distance between sensors calculated by arrival of signal