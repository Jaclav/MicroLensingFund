import sys
import numpy as np
(time,mag,r)=np.loadtxt(sys.argv[1], unpack=True)
indeksy=np.argsort(mag)
print(time[indeksy[5]])
