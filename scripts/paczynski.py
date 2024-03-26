from math import *
import matplotlib.pyplot as plt

dom = [i / 10 for i in range(-100000, 100000)]


def calculate(domain, fun):
    values = []
    for i in range(len(domain)):
        f = fun(domain[i])
        if f > 10 or f < -10:
            f = nan
        values.append(f)
    return values

t0 = 4087.35681
u0 = 0.51782
tE = 311.68956
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
