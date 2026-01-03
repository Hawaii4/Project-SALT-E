import math as math
import matplotlib.pyplot as plt

#reference sensor set as sensor1

speed_of_sound = 346

class Sensor:
    def __init__(self):
        self.coords = [0,0]
        self.t = 0
        self.dist_to_source = 0

    def setcoords(self, x, y):
        self.coords = [x,y]

    def sett(self, t):
        self.t = t

    def getdist_source(self):
        self.dist_to_source = self.t * speed_of_sound

    def dist_diff(self, compare):
        return compare - self.dist_to_source

    def m(self):
        m = 0.5*((math.sqrt(self.coords[0]**2 + self.coords[1]**2))**2 - (math.sqrt(s1.coords[0]**2 + s1.coords[1]**2))**2 - self.dist_diff(s1.dist_to_source)**2)
        return m

s1 = Sensor()
s1.setcoords(4,6)
s1.sett(1.05)
s1.getdist_source()


s2 = Sensor()
s2.setcoords(2,9)
s2.sett(1.0625)
s2.getdist_source()

s3 = Sensor()
s3.setcoords(7,8)
s3.sett(1.0416)
s3.getdist_source()

print(s3.dist_diff(s1.dist_to_source)*(s2.coords[1]-s1.coords[1]), "da")
print(-s2.dist_diff(s1.dist_to_source)*(s3.coords[1]-s1.coords[1]), "da")
alpha = (s2.dist_diff(s1.dist_to_source)*(s3.coords[0]-s1.coords[0]) - s3.dist_diff(s1.dist_to_source)*(s2.coords[0]-s1.coords[0]))/(-s2.dist_diff(s1.dist_to_source)*(s3.coords[1]-s1.coords[1])+s3.dist_diff(s1.dist_to_source)*(s2.coords[1]-s1.coords[1]))
beta = (s3.dist_diff(s1.dist_to_source)*s1.m()-s2.dist_diff(s1.dist_to_source)*s2.m())/(-s2.dist_diff(s1.dist_to_source)*(s3.coords[1]-s1.coords[1])-s3.dist_diff(s1.dist_to_source)*(s2.coords[1]-s1.coords[1]))

print("alpha = ", alpha)
print("beta = ", beta)

a = ((1+alpha**2)-((s2.coords[0] - s1.coords[0]) + (s2.coords[1] - s1.coords[1])*alpha)**2) / (s2.dist_diff(s1.dist_to_source)**2)
b = -2*((s1.coords[0] + (s1.coords[1] - beta)*alpha) - ((s2.coords[0] - s1.coords[0]) + (s2.coords[1] - s1.coords[1])*alpha)*((s2.coords[1] - s1.coords[1])*beta - s1.m()))
c = (s1.coords[1] - beta)**2 + s1.coords[0]**2 - (((s2.coords[1] - s1.coords[1])*beta - s1.m()) / (s2.dist_diff(s1.dist_to_source)**2))**2

print(a)
print(b)
print(c)

xs1 = (-b + math.sqrt(b**2 - 4*a*c))/(2*a)
xs2 = (-b - math.sqrt(b**2 - 4*a*c))/(2*a)
ys1 = alpha*xs1 + beta
ys2 = alpha*xs2 + beta

print(xs1, "green")
print(ys1)
print(xs2, "red")
print(ys2)

x_vals = [xs1, s1.coords[0]]
y_vals = [ys1, s1.coords[1]]

x_vals2 = [xs2, s1.coords[0]]
y_vals2 = [ys2, s1.coords[1]]

plt.figure(figsize=(10,10))
plt.xlim(-10,10)
plt.ylim(-10,10)
plt.plot(s1.coords[0], s1.coords[1], 'o', color='red')
plt.plot(s2.coords[0], s2.coords[1], '1', color='blue')
plt.plot(s3.coords[0], s3.coords[1], 'x', color='blue')
plt.title("{s}/{h}, {y}/{w}".format(s=xs1, h=xs2, y=ys1, w=ys2))
plt.plot(x_vals, y_vals, ls=":", color='green')
plt.plot(x_vals2, y_vals2, ls="--", color='red')
#plt.plot(xs1, ys1, 'o', color='green')
#plt.plot(xs2, ys2, 'o', color='green')
plt.grid(True)
plt.show()
plt.close()


## why can't the sound come from the other side?
## this program is for fixed coordinates of the sensors -> don't understand why it can only be those two points
## program 3Mic_2d_dot.py for distance between sensors calculated by arrival of signal