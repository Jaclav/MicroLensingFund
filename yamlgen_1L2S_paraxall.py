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
os.mkdir("../" + sys.argv[1] + "/1L2S_paraxall")
os.mkdir("../" + sys.argv[1] + "/1L2S_paraxall/png")

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
                u0 = float(tab["u_0"])
                tE = float(tab["t_E"])
                xi_period = float(tab["xi_period"])
                break

    newFile = xallarapName[i]
    yamlN = "../" + sys.argv[1] + "/1L2S_paraxall/" + newFile + ".yaml"
    yaml = open(yamlN, "w+")
    t0par = round(t0, -1)
    graphicF = sys.argv[1] + "/1L2S_paraxall/png/" + newFile
    YAML = [
        "photometry_files:",
        "    dataPoleski/" + xallarapName[i],
        "starting_parameters:",
        "    t_0: gauss " + str(t0) + " 0.1",
        "    u_0: gauss " + str(u0) + " " + str(0.3 * u0),
        "    t_E: gauss " + str(tE) + " " + str(tE * 0.1),
        # parallax piE=sqrt(PiN^2+pIEE^2)
        "    pi_E_N: gauss 0.00 0.01",
        "    pi_E_E: gauss 0.00 0.01",
        # PARAXALL https://doi.org/10.3847/1538-3881/ad284f
        "    xi_Omega_node: uniform -20 380",
        "    xi_inclination: uniform -20 380",
        "    xi_period: log-uniform 50 500",
        "    xi_argument_of_latitude_reference: uniform -20 380",
        "    xi_semimajor_axis: log-uniform 0.01 0.5",
        "    q_source: log-uniform 0.001 0.5",
        "    xi_eccentricity: log-uniform 0.01 1",
        "    xi_omega_periapsis: uniform -20 380",
        # parallax
        "model:",
        "   coords: " + right_ascension[i] + " " + declination[i],
        "fixed_parameters:",
        "    t_0_par: " + str(t0par),
        "    t_0_xi: " + str(t0par),
        "min_values:",
        "    u_0: 0.",
        "    t_E: 0.",
        "    xi_semimajor_axis: 0.",
        "    xi_period: 0.",
        "    xi_Omega_node: -20.",
        "    xi_inclination: -20.",
        "    xi_argument_of_latitude_reference: -20.",
        "    pi_E_N: -1.",
        "    pi_E_E: -1.",
        "    q_source: 0.",
        "    xi_eccentricity: 0.",
        "    xi_omega_periapsis: -20.",
        "max_values:",
        "    xi_Omega_node: 380.",
        "    xi_inclination: 380.",
        "    xi_argument_of_latitude_reference: 380.",
        "    pi_E_N: 1.",
        "    pi_E_E: 1.",
        "    xi_eccentricity: 1.",
        "    xi_omega_periapsis: 380.",
        "fitting_parameters:",
        "    n_steps: 5000",
        "    n_walkers: 1000",
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
