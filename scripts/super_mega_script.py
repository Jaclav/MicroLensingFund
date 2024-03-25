import sys
import numpy as np

(time,mag,r)=np.loadtxt(sys.argv[1], unpack=True)
indeksy=np.argsort(mag)
time[indeksy[5]]

tE = np.zeros(indeksy.size)
A = np.zeros(indeksy.size)
u = np.zeros(indeksy.size)

for i in range(indeksy.size):
    A[i] = 10**(-0.4*(mag[indeksy[i]] - mag[indeksy[-5]]))
    u[i] = np.sqrt(2) * np.sqrt(
    1 / (-1 + A[i]**2) - A[i]**2 / (-1 + A[i]**2) + np.sqrt(A[i]**2 * (-1 + A[i]**2)) / (-1 + A[i]**2)
    )
    tE[i] = abs(time[indeksy[i]] - time[indeksy[5]]) / (np.sqrt(u[i]**2 - u[5]**2))
