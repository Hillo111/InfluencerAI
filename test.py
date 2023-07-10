import random
from time import sleep
from math import *
def f():
    return max(random.random() ** 3 * 4, 1)

t = 0
n = 100000
for i in range(n):
    t += f()
print(t / n)