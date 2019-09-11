
from math import exp as e
import random
import math

RADIUS = 0.5
INITIAL_POINT = (2,2)
T0 = 1

def schedule(t):
    return T0*e(-t/1000)

def F(point):
    x,y = point
    return 4*e(-(x**2+y**2))+e(-((x-5)**2+(y-5)**2))+e(-((x+5)**2+(y-5)**2))+e(-((x-5)**2+(y+5)**2))+e(-((x+5)**2+(y+5)**2))

def simulated_annealing():
    current = INITIAL_POINT
    t = 0
    while True:
        T = schedule(t)
        x,y = current
        if T == 0:
            print(F(current),t)
            return current
        angle = random.uniform(-180,180)*math.pi/180
        next = (x + RADIUS*math.cos(angle), y + RADIUS*math.sin(angle))
        dE = F(next) - F(current)
        if dE > 0:
            current = next
        else:
            p = e(dE/T)
            current = next if random.random() < p else current
        t = t+1

print(simulated_annealing())