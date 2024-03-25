import sys
import numpy as np

(time,mag,r)=np.loadtxt(sys.argv[1], unpack=True)
indeksy=np.argsort(mag)

t0 = time[indeksy[5]]

A0 = 10**(-0.4*(mag[indeksy[5]] - mag[indeksy[-5]]))

u0 = np.sqrt(2) * np.sqrt(
    1 / (-1 + A0**2) - A0**2 / (-1 + A0**2) + np.sqrt(A0**2 * (-1 + A0**2)) / (-1 + A0**2)
)

tE = np.zeros(indeksy.size)
A = np.zeros(indeksy.size)
u = np.zeros(indeksy.size)

for i in range(indeksy.size):
    A[i] = 10**(-0.4*(mag[indeksy[i]] - mag[indeksy[-5]]))
    u[i] = np.sqrt(2) * np.sqrt(
    1 / (-1 + A[i]**2) - A[i]**2 / (-1 + A[i]**2) + np.sqrt(A[i]**2 * (-1 + A[i]**2)) / (-1 + A[i]**2)
    )
    tE[i] = abs(time[indeksy[i]] - t0) / (np.sqrt(u[i]**2 - u0**2))

tEfinal = np.mean(tE)

print(t0,"  ",u0,"  ",tEfinal,"  ",A0)