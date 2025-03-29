import os
import random as r
import sys
import numpy as np

(name, right_ascension, declination) = np.loadtxt(
    "parallaxData/coords.csv", unpack=True, delimiter=",", dtype=str
)

os.mkdir(sys.argv[1] + "/parallax")
os.mkdir(sys.argv[1] + "/parallax/png")
os.chdir("dataPoleski")
listFiles = os.listdir()
for index, file in enumerate(listFiles):

    with open("../" + sys.argv[1] + "/nothing/" + file + ".OUT", "r") as fileOUT:
        print("../" + sys.argv[1] + "/nothing/" + file + ".OUT")
        lines = fileOUT.readlines()
        param_vals = lines[:][12]
        param_vals_list = param_vals.split()
        t0 = float(param_vals_list[0])
        u0 = float(param_vals_list[1])
        tE = 100

    for sign in ["+", "-"]:
        newFile = file + sign
        yamlN = "../" + sys.argv[1] + "/parallax/" + newFile + ".yaml"
        yaml = open(yamlN, "w+")
        t0par = round(t0, -1)
        graphicF = sys.argv[1] + "/parallax/png/" + newFile
        YAML = [
            "photometry_files:",
            "    dataPoleski/" + file,
            "starting_parameters:",
            "    t_0: gauss " + str(t0) + " 0.1",
            "    u_0: gauss " + sign + str(u0) + " 0.01",
            "    t_E: gauss " + str(tE) + " " + "10",
            # parallax
            "    pi_E_N: gauss 0.0 0.1",
            "    pi_E_E: gauss 0.0 0.1",
            # parallax
            "model:",
            "   coords: " + right_ascension[index] + " " + declination[index],
            "fixed_parameters:",
            "    t_0_par: " + str(t0par),
            "min_values:",
            ("    u_0: 0." if sign == "+" else ""),
            ("    u_0: -5." if sign == "-" else ""),
            "    t_E: 0.",
            "    pi_E_N: -1.",
            "    pi_E_E: -1.",
            "max_values:",
            ("    u_0: 0." if sign == "-" else ""),
            ("    u_0: 5." if sign == "+" else ""),
            "    pi_E_N: 1.",
            "    pi_E_E: 1.",
            "fitting_parameters:",
            "    n_steps: 30000",
            "    n_walkers: 20",
            "fit_constraints:",
            "    negative_blending_flux_sigma_mag: 20.",
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
