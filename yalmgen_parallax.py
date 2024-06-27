import os
import random as r
import sys
import numpy as np

# run: ./yamlgen.sh P1
(name, right_ascension, declination) = np.loadtxt(
    "parallaxData/coords.csv", unpack=True, delimiter=",", dtype=str
)

os.mkdir(sys.argv[1] + "/parallax")
os.mkdir(sys.argv[1] + "/parallax/png")
os.chdir("dataPoleski")
listFiles = os.listdir()
for index, file in enumerate(listFiles):
    parN = "../" + sys.argv[1] + "/nothing/" + file + ".par"
    (PARt0, PARu0, PARtE, PARA, PARtmin, PARtmax) = np.loadtxt(parN)

    with open("../" + sys.argv[1] + "/nothing/" + file + ".OUT", "r") as fileOUT:
        print("../" + sys.argv[1] + "/nothing/" + file + ".OUT")
        lines = fileOUT.readlines()
        string = lines[3][6:]
        t0 = float(string[3 : string[3:].find(" ")])
        string = lines[4][6:]
        u0 = float(string[: string.find(" ")])
        if abs(u0) > 2.0:
            print("U:" + file)
            u0 = 0.0
        string = lines[5][6:]
        tE = float(string[: string.find(" ")])
        if tE > 1000.0:
            print("E:" + file)
            tE = 100.0
        print(t0, " ", u0, " ", tE)

    for sign in ["+", "-"]:
        newFile = file + sign
        yamlN = "../" + sys.argv[1] + "/parallax/" + newFile + ".yaml"
        yaml = open(yamlN, "w+")
        t0par = round(t0, -1)
        graphicF = sys.argv[1] + "/parallax/png/" + newFile
        tmin = PARtmin
        tmax = PARtmax
        YAML = [
            "photometry_files:",
            "    dataPoleski/" + file,
            "starting_parameters:",
            "    t_0: gauss 245" + str(t0) + " 0.1",
            "    u_0: gauss " + sign + str(u0) + " " + str(0.3 * u0),
            "    t_E: gauss " + str(tE) + " " + str(tE * 0.5),
            # parallax
            "    pi_E_N: gauss 0.00 0.01",
            "    pi_E_E: gauss 0.00 0.01",
            # parallax
            "model:",
            "   coords: " + right_ascension[index] + " " + declination[index],
            "fixed_parameters:",
            "    t_0_par: 245" + str(t0par),
            "min_values:",
            ("    u_0: 0." if sign == "+" else ""),
            "    t_E: 0.",
            "    pi_E_N: -1.",
            "    pi_E_E: -1.",
            "max_values:",
            ("    u_0: 0." if sign == "-" else ""),
            "    pi_E_N: 1.",
            "    pi_E_E: 1.",
            "fitting_parameters:",
            "    n_steps: 10000",
            "    n_walkers: 20",
            "plots:",
            "    best model:",
            "        file: " + graphicF + ".png",
            "    trajectory:",
            "        file: " + graphicF + ".trj.png",
            "    triangle:",
            "        file: " + graphicF + ".trg.png",
            "    trace:",
            "        file: " + graphicF + ".tra.png",
        ]
        for line in YAML:
            yaml.writelines(line + "\n")
