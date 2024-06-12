import os
import sys
import numpy as np
from pathlib import Path
import pandas as pd


dat = pd.read_csv(
    "./"+sys.argv[1] + "/chi2_with_paraxall.csv", delimiter=",", dtype=str, header=None
)
for i in range(0, 9):
    dat[i].pop(0)

name = dat[0]
better = dat[1]
parallaxPath = dat[3]
xallarapPath = dat[5]
pathParaxall = dat[8]

listFiles = []
listNames = []
for i in range(1, len(name)+1):
    if better[i] == "xallarap":
        listFiles.append(pathParaxall[i])
        listNames.append(pathParaxall[i][15:21])
    else:
         listFiles.append(np.nan)
         listNames.append(np.nan)
         
table = open("Presentation/table_Xi_period.csv", "w")
table.write("Nazwa - OGLE3-ULENS- & $xi_{period}$ & $\pi_{EN}$ & $\pi_{EE}$ \\\ \n")

for index, file in enumerate(listNames):
    if type(listFiles[index]) == str:
        f = open(listFiles[index],"r")
        lines = f.readlines()
        for line in lines:
            if "t_0" in line and "u_0" in line:
                    pass    
            elif "xi_period" in line:
                xi_p = float(line.split()[2])
                xi_p = round(xi_p, 3)
                xi_pp = float(line.split()[3])
                xi_pp = round(xi_pp, 2)
                xi_pm = float(line.split()[4])
                xi_pm = round(xi_pm, 2)
            elif "pi_E_N" in line:
                pi_E_N = float(line.split()[2])
                pi_E_N = round(pi_E_N, 3)
                pi_E_N_p = float(line.split()[3])
                pi_E_N_p = round(pi_E_N_p, 2)
                pi_E_N_m = float(line.split()[4])
                pi_E_N_m = round(pi_E_N_m, 2)
            elif "pi_E_E" in line:
                pi_E_E = float(line.split()[2])
                pi_E_E = round(pi_E_E, 3)
                pi_E_E_p = float(line.split()[3])
                pi_E_E_p = round(pi_E_E_p, 2)
                pi_E_E_m = float(line.split()[4])
                pi_E_E_m = round(pi_E_E_m, 2)
                
                
        table.write(file+"& $" + str(xi_p) + "_{" + str(xi_pm) + " } ^{+" + str(xi_pp) + "}$" + "& $" + str(pi_E_N) + "_{" + str(pi_E_E_m) + " } ^{+" + str(pi_E_N_p) + "}$" + "& $" + str(pi_E_N) + "_{" + str(pi_E_E_m) + " } ^{+" + str(pi_E_N_p) + "}$ \\\ \n")
                
        