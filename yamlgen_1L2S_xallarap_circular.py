import os
import random as r
import sys
import numpy as np

# run: ./yamlgen.sh P1
os.chdir("dataPoleski")
(name, right_ascension, declination) = np.loadtxt(
    "../" + "/parallaxData/coords.csv",
    unpack=True,
    delimiter=",",
    dtype=str,
)
indeks = -1
os.mkdir("../" + sys.argv[1] + "/1L2S_xallarap_circular")
os.mkdir("../" + sys.argv[1] + "/1L2S_xallarap_circular/png")

(name, better, parallax, parallaxPath, xallarap, xallarapPaths, deltaChi) = np.loadtxt(
    "../" + sys.argv[1] + "/chi2.csv", unpack=True, delimiter=",", dtype=str, skiprows=1
)
xallarapName = []
xallarapPath = []
for i in range(len(name)):
    if better[i] == "xallarap":
        xallarapPath.append(xallarapPaths[i])
        xallarapName.append(name[i])
# katalog z xalarap
for i in range(len(xallarapPath)):
    with open(xallarapPath[i], "r") as fileOUT:
        print(fileOUT.name)
        lines = fileOUT.readlines()
        for k in range(len(lines)):
            if "t_0" in lines[k] and "u_0" in lines[k]:
                keys = lines[k].split()
                vals = lines[k + 1].split()
                tab = {}
                for j in range(len(keys)):
                    tab[keys[j]] = vals[j]
                t0 = float(tab["t_0"])
                u0 = abs(float(tab["u_0"]))
                tE = float(tab["t_E"])
                xi_period = float(tab["xi_period"])
                xi_a = float(tab["xi_semimajor_axis"])
                xi_Omega = float(tab["xi_Omega_node"])
                xi_i = float(tab["xi_inclination"])
                xi_u = float(tab["xi_argument_of_latitude_reference"])

                u0_err = 10**(int(np.log10(abs(u0)))-4)
                break

    newFile = xallarapName[i]
    yamlN = "../" + sys.argv[1] + "/1L2S_xallarap_circular/" + newFile + ".yaml"
    yaml = open(yamlN, "w+")
    graphicF = sys.argv[1] + "/1L2S_xallarap_circular/png/" + newFile
    YAML = [
        "photometry_files:",
        "    dataPoleski/" + xallarapName[i],
        "starting_parameters:",
        "    t_0: gauss " + str(t0) + " 0.01",
        "    u_0: gauss " + str(u0) + " " + format(u0_err, '.10f'),
        "    t_E: gauss " + str(tE) + " " + "0.01",
        # PARAXALL https://doi.org/10.3847/1538-3881/ad284f
        "    xi_period: gauss " + str(xi_period) + " 1.0",
        "    xi_semimajor_axis: gauss " + str(xi_a) + " 1.0",
        "    xi_Omega_node: gauss " + str(xi_Omega) + " 1.0",
        "    xi_inclination: gauss " + str(xi_i) + " 1.0",
        "    xi_argument_of_latitude_reference: gauss " + str(xi_u) + " 1.0",
        "    q_source: log-uniform 0.001 0.5",
        # parallax
        "model:",
        "   coords: " + right_ascension[i] + " " + declination[i],
        "fixed_parameters:",
        "    t_0_xi: " + str(round(t0)),
        "min_values:",
        "    u_0: 0.",
        "    t_E: 0.",
        "    xi_semimajor_axis: 0.",
        "    xi_period: 0.",
        "    xi_Omega_node: -20.",
        "    xi_inclination: -20.",
        "    xi_argument_of_latitude_reference: -20.",
        "    q_source: 0.",
        "max_values:",
        "    xi_Omega_node: 380.",
        "    xi_inclination: 380.",
        "    xi_argument_of_latitude_reference: 380.",
        "fitting_parameters:",
        "    n_steps: 20000",
        "    n_walkers: 40",
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
        yaml.writelines(str(line) + "\n")