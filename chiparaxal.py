import numpy as np
import os
import glob
import sys


def getChi(name):
    with open(name, "r") as file:
        lines = file.readlines()
    for i in lines:
        if i[:5] == "chi2:":
            return float(i[6:-1])
    return 1000000


a = np.loadtxt(sys.argv[1] + "/chi2.csv", skiprows=1, unpack=True, dtype=str)
data = {}

paraxals = []
for p in glob.glob(sys.argv[1] + "/paraxall/*.OUT"):
    paraxals.append(p.split("/")[2].split(".")[0] + ".dat")

for i in a:
    name = i.split(",")[0]
    if name in paraxals:
        chip = getChi(sys.argv[1] + "/paraxall/" + name + "+.OUT")
        chim = getChi(sys.argv[1] + "/paraxall/" + name + "-.OUT")
        path = ""
        chi = 0

        if chip > chim:
            chi = chim
            path = sys.argv[1] + "/paraxall/" + name + "-.OUT"
        else:
            chi = chip
            path = sys.argv[1] + "/paraxall/" + name + "+.OUT"
        print(i + "," + str(chi) + "," + path)
    else:
        print(i)
# python3 chiparaxal.py sim28 > sim28/chi2_with_paraxall.csv