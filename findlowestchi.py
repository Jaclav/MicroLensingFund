import os
import random as r
import sys
import numpy as np


listF = os.listdir("../" + sys.argv[1] + "/yaml")
chilist = []
indeks = 0
for file in listF:
    if file[::5] == file[::5] and file[::-3] == ".OUT":
        indeks += 1
        with open(f"{f}") as in_file:
                file = in_file

        for line in file:
            line.readline()
            wyrazy = line.split()
            if wyrazy[0] == "chi2":
                 chilist.append(float(wyrazy[2]))
        lowest_chi=chilist.argsort()[-1]
        if indeks < 10:
            print(f"PAR-0" + str(indeks)+"-noaver.dat."+f"{lowest_chi}"+".yaml")
        else:
             print(f"PAR-" + str(indeks)+"-noaver.dat."+f"{lowest_chi}"+".yaml")
        chilist = []

