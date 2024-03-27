import os
import random as r
import sys
import numpy as np

plik=open("lowestchi.txt",'w')
listF = os.listdir("../" + sys.argv[1] + "/yaml")
chilist = []
indeks = 0
for file in listF:
    if file[::5] == file[::5] and file[::-3] == ".OUT":
        indeks += 1
        with open(file) as in_file:
            file_content = in_file.readlines()

        for line in file_content:
            wyrazy = line.split()
            if wyrazy[0] == "chi2":
                chilist.append(float(wyrazy[2]))
        lowest_chi = chilist.argsort()[-1]
        if indeks < 10:
            plik.write(f"PAR-0{indeks}-noaver.dat.{lowest_chi}.yaml")
        else:
            plik.write(f"PAR-{indeks}-noaver.dat.{lowest_chi}.yaml")
        chilist = []
plik.close()



