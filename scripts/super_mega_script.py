from statistics import median
import sys
import numpy as np

(time, mag, r) = np.loadtxt(sys.argv[1], unpack=True)
indeksy = np.argsort(mag)

t0 = time[indeksy[5]]

A0 = 10 ** (-0.4 * (mag[indeksy[5]] - mag[indeksy[-5]]))

u0 = np.sqrt(2) * np.sqrt(
    1 / (-1 + A0**2)
    - A0**2 / (-1 + A0**2)
    + np.sqrt(A0**2 * (-1 + A0**2)) / (-1 + A0**2)
)

tE = np.zeros(indeksy.size)
for i in range(indeksy.size):
    j = indeksy[i]
    A = 10 ** (-0.4 * (mag[j] - mag[indeksy[-5]]))

    u = np.sqrt(2) * np.sqrt(
        1 / (-1 + A**2) - A**2 / (-1 + A**2) + np.sqrt(A**2 * (-1 + A**2)) / (-1 + A**2)
    )
    tE[j] = abs(time[j] - t0) / (np.sqrt(abs(u**2 - u0**2)))

for i in range(indeksy.size):
    if np.isnan(tE[i]):
        tE[i] = tE[i - 1]
    else:
        continue

tEfinal = median(tE)

print(t0, "  ", u0, "  ", tEfinal, "  ", A0, "  ", time[0], "  ", time[-1])
