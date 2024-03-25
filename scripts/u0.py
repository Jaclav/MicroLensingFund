import sys
import numpy as np

(time, mag, r) = np.loadtxt(sys.argv[1], unpack=True)
indeksy = np.argsort(mag)

A = 10**(-0.4*(mag[indeksy[5]] - mag[indeksy[-5]]))

u = np.sqrt(2) * np.sqrt(
    1 / (-1 + A**2) - A**2 / (-1 + A**2) + np.sqrt(A**2 * (-1 + A**2)) / (-1 + A**2)
)

print(u)