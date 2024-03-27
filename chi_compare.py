import os
import random as r
import sys
import numpy as np

plik=open("chi2table.csv","w+")

os.chdir("dataPoleski")
Names = os.listdir()

folder_simulation = sys.argv[1]

#NOTHING
os.chdir(folder_simulation + "/nothing")

listFiles_nothing = Names

for i in range(len(Names)):
    listFiles_nothing.append(Names[i] + ".OUT")

for i in range(len(listFiles_nothing)):
    f = open(listFiles_nothing[i], "r")
    lines = f.readlines()
    chi2_table_nothing = []
    for j in range(len(lines)):
        if "chi2" in lines[j]:
            chi2_table_nothing.append(float(lines[j].split()[1]))
    f.close()

#PARALLAX
os.chdir("../parallax")

listFiles_parallaxp = Names

listFiles_parallaxm = Names


for i in range(len(Names)):
    listFiles_parallaxp.append(Names[i] + "+.OUT")
    listFiles_parallaxm.append(Names[i] + "-.OUT")

    f = open(listFiles_parallaxp[i], "r")
    lines = f.readlines()
    chi2_table_parallaxp = []
    for j in range(len(lines)):
        if "chi2" in lines[j]:
            chi2_table_parallaxp.append(float(lines[j].split()[1]))
    f.close()

    f = open(listFiles_parallaxm[i], "r")
    lines = f.readlines()
    chi2_table_parallaxm = []
    for j in range(len(lines)):
        if "chi2" in lines[j]:
            chi2_table_parallaxm.append(float(lines[j].split()[1]))
    f.close()

    chi2_table_parallax = []

    for j in range(len(chi2_table_parallaxp)):
        if chi2_table_parallaxp[j] < chi2_table_parallaxm[j]:
            chi2_table_parallax[j] = chi2_table_parallaxp[j]
        else:
            chi2_table_parallax[j] = chi2_table_parallaxm[j]

#XALLARAP
os.chdir("../xallarap")

listFiles_xallarap_temp = np.zeroes((len(Names),10))
listFiles_xallarap =[]

for i in range(len(Names)):
    for j in range(10):
        listFiles_xallarap.append(Names[i] + "." + str(j) + ".OUT")
        f = open(listFiles_xallarap[i,j], "r")
        lines = f.readlines()
        chi2_table_xallarap = []
        for k in range(len(lines)):
            if "chi2" in lines[k]:
                chi2_table_xallarap.append(float(lines[k].split()[1]))
        f.close()
        listFiles_xallarap_temp[i,j] = chi2_table_xallarap[j]

for i in range(len(Names)):
    for j in range(10):
        if listFiles_xallarap_temp[i,j] < chi2_table_xallarap[i]:
            chi2_table_xallarap[i] = listFiles_xallarap_temp[i,j]


for i in range(len(Names)):
    plik.write(Names[i] + "," + chi2_table_nothing[i] + "," + chi2_table_parallax[i] + "," + chi2_table_xallarap[i] + "," + "\n")



