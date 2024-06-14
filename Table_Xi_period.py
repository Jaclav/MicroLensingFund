import os
import sys
import numpy as np
from pathlib import Path
import pandas as pd
import string
string.punctuation


         
table = open("Presentation/table_Xi_period.csv", "w")

file = "sim30/paraxall/PAR-06-noaver.dat-.OUT"

f = open(file,"r")
lines = f.readlines()
for line in lines:
    if "t_0" in line and "u_0" in line:
            pass    
    elif "t_0" in line:
        t_0 = float(line.split()[2])
        t_0 = round(t_0, 3)
        t_0_p = float(line.split()[3])
        t_0_p = round(t_0_p, 2)
        t_0_m = float(line.split()[4])
        t_0_m = round(t_0_m, 2)
    elif "u_0" in line:
        u_0 = float(line.split()[2])
        u_0 = round(u_0, 3)
        u_0_p = float(line.split()[3])
        u_0_p = round(u_0_p, 2)
        u_0_m = float(line.split()[4])
        u_0_m = round(u_0_m, 2)
    elif "t_E" in line:
        t_E = float(line.split()[2])
        t_E = round(t_E, 3)
        t_E_p = float(line.split()[3])
        t_E_p = round(t_E_p, 2)
        t_E_m = float(line.split()[4])
        t_E_m = round(t_E_m, 2)
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
    elif "xi_semimajor_axis" in line:
        xi_semimajor_axis = float(line.split()[2])
        xi_semimajor_axis = round(xi_semimajor_axis, 3)
        xi_semimajor_axis_p = float(line.split()[3])
        xi_semimajor_axis_p = round(xi_semimajor_axis_p, 2)
        xi_semimajor_axis_m = float(line.split()[4])
        xi_semimajor_axis_m = round(xi_semimajor_axis_m, 2)

table.write("Parametr  & wartość \\\ \n")
table.write("t_0 & $" + str(t_0) + "_{" + str(t_0_m) + " } ^{+" + str(t_0_p) + "}$ \\\ \n")
table.write("u_0 & $" + str(u_0) + "_{" + str(u_0_m) + " } ^{+" + str(u_0_p) + "}$ \\\ \n")
table.write("t_E & $" + str(t_E) + "_{" + str(t_E_m) + " } ^{+" + str(t_E_p) + "}$ \\\ \n")
table.write("$\\pi_{EN}$ & $" + str(pi_E_N) + "_{" + str(pi_E_N_m) + " } ^{+" + str(pi_E_N_p) + "}$ \\\ \n")
table.write("$\\pi_{EE}$ & $" + str(pi_E_E) + "_{" + str(pi_E_E_m) + " } ^{+" + str(pi_E_E_p) + "}$ \\\ \n")
table.write("$\\xi_{period}$ & $" + str(xi_p) + "_{" + str(xi_pm) + " } ^{+" + str(xi_pp) + "}$ \\\ \n")
table.write("$\\xi_{semimajor axis}$ & $" + str(xi_semimajor_axis) + "_{" + str(xi_semimajor_axis_m) + " } ^{+" + str(xi_semimajor_axis_p) + "}$ \\\ \n")
table.close()
