from math import *
import matplotlib.pyplot as plt
import sys

dom = [i / 10 for i in range(-100000, 100000)]


def calculate(domain, fun):
    values = []
    for i in range(len(domain)):
        f = fun(domain[i])
        if f > 1000 or f < -1000:
            f = nan
        values.append(f)
    return values


lines = []
with open(sys.argv[1], "r") as file:
    lines = file.readlines()
str = lines[3][6:]
t0 = float(str[3 : str[3:].find(" ")])
str = lines[4][6:]
u0 = float(str[: str.find(" ")])
str = lines[5][6:]
tE = float(str[: str.find(" ")])
print(t0, " ", u0, " ", tE)

plt.plot(
    dom,
    calculate(
        dom,
        lambda x: (sqrt(u0**2 + ((x - t0) / tE) ** 2) ** 2 + 2)
        / (
            sqrt(u0**2 + ((x - t0) / tE) ** 2)
            * sqrt(sqrt(u0**2 + ((x - t0) / tE) ** 2) ** 2 + 4)
        ),
    ),
)
plt.show()
