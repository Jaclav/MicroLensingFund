import os
import random as r
import sys
import numpy as np

# run: ./yamlgen.sh P1
(name, right_ascension, declination) = np.loadtxt(
    "parallaxData/coords.csv", unpack=True, delimiter=",", dtype=str
)
indeks = -1
os.mkdir(sys.argv[1] + "/parallax")
os.mkdir(sys.argv[1] + "/parallax/png")
os.chdir("dataPoleski")
listFiles = os.listdir()
for file in listFiles:
    parN = "../" + sys.argv[1] + "/nothing/" + file + ".par"
    (PARt0, PARu0, PARtE, PARA, PARtmin, PARtmax) = np.loadtxt(parN)

    listF = os.listdir("../" + sys.argv[1] + "/yaml")
    with open("../" + sys.argv[1] + "/nothing/" + file + ".OUT", "r") as fileOUT:
        print("../" + sys.argv[1] + "/nothing/" + file + ".OUT")
        lines = fileOUT.readlines()
        string = lines[3][6:]
        t0 = float(string[3 : string[3:].find(" ")])
        string = lines[4][6:]
        u0 = float(string[: string.find(" ")])
        string = lines[5][6:]
        tE = float(string[: string.find(" ")])
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
            "    pi_E_N: uniform -1.0 1.0",
            "    pi_E_E: uniform -1.0 1.0",
            # parallax
            "model:",
            "   coords: " + right_ascension[indeks] + " " + declination[indeks],
            "fixed_parameters:",
            "    t_0_par: 245" + str(t0par),
            "min_values:",
            "    u_0: 0.",
            "    t_E: 0.",
            "fitting_parameters:",
            "    n_steps: 50000",
            "    n_walkers: 20",
            "plots:",
            "    best model:",
            "        file: " + graphicF + ".png",
            "        time range: 245" + str(tmin) + " 245" + str(tmax),
            "    trajectory:",
            "        file: " + graphicF + ".trj.png",
            "        time range: 245" + str(tmin) + " 245" + str(tmax),
            "    triangle:",
            "        file: " + graphicF + ".trg.png",
            "    trace:",
            "        file: " + graphicF + ".tra.png",
        ]
        for line in YAML:
            yaml.writelines(line + "\n")
