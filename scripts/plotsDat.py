import matplotlib.pyplot as plt
import numpy as np
import sys
#ls | while read a; do python3 ../scripts/plotsDat.py $a; done

(time, mag, r) = np.loadtxt(sys.argv[1], unpack=True)

plt.gca().invert_yaxis()
# plt.errorbar(time, mag, r)
plt.errorbar(time, mag, r, marker="s", mfc="red", mec="black", ms=4, mew=1)
plt.title("Mag(t)")
# plt.show()
plt.savefig(sys.argv[1] + ".png")
