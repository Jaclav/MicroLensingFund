import os
import random as r
import sys
import numpy as np

# run: ./yamlgen.sh P1
(name, right_ascension, declination) = np.loadtxt(
    "parallaxData/coords.csv", unpack=True, delimiter=",", dtype=str
)
indeks = -1
os.mkdir(sys.argv[1] + "/paraxall")
os.mkdir(sys.argv[1] + "/paraxall/png")
# os.mkdir(sys.argv[1] + "/paraxallData")
os.chdir(sys.argv[1])

(name, better, parallax, parallaxPath, xallarap, xallarapPath, deltaChi) = np.loadtxt(
    sys.argv[1] + "/chi2.csv", unpack=True, delimiter=",", dtype=str
)

xallarapnames = []

for i in range(len(name)):
    if better[i] == "xalllarap":
        xallarapnames.append(xallarapPath[i])
# katalog z xalarap

for i in range(len(xallarapnames)):
    parN = sys.argv[1] + "/nothing/" + xallarapnames[i] + ".par"
    (PARt0, PARu0, PARtE, PARA, PARtmin, PARtmax) = np.loadtxt(parN)
    #
    with open(
        "../" + sys.argv[1] + "/nothing/" + xallarapnames[i] + ".OUT", "r"
    ) as fileOUT:
        print("../" + sys.argv[1] + "/nothing/" + xallarapnames[i] + ".OUT")
        lines = fileOUT.readlines()
        string = lines[3][6:]
        t0 = float(string[3 : string[3:].find(" ")])
        string = lines[4][6:]
        u0 = float(string[: string.find(" ")])
        string = lines[5][6:]
        tE = float(string[: string.find(" ")])
        print(t0, " ", u0, " ", tE)
    # tutaj sie zatrzymałem
    for n in range(1, 11):
        for sign in ["+", "-"]:
            newFile = xallarapnames + "." + str(n) + sign
            yamlN = "../" + sys.argv[1] + "/PARAXALL/" + newFile + ".yaml"
            yaml = open(yamlN, "w+")
            xi_P = r.gauss((80 ** ((n - 1) / 9)) * 5, 0.001)
            t0par = round(t0, -1)
            graphicF = sys.argv[1] + "/PARAXALL/png/" + newFile
            tmin = PARtmin
            tmax = PARtmax
            YAML = [
                "photometry_files:",
                "    dataPoleski/" + xallarapnames,
                "starting_parameters:",
                "    t_0: gauss 245" + str(t0) + " 0.1",
                "    u_0: gauss " + sign + str(u0) + " " + str(0.3 * u0),
                "    t_E: gauss " + str(tE) + " " + str(tE * 0.5),
                # parallax
                "    pi_E_N: gauss 0.00 0.01",
                "    pi_E_E: gauss 0.00 0.01",
                # PARAXALL https://doi.org/10.3847/1538-3881/ad284f
                "    xi_Omega_node: uniform -20 380",
                "    xi_inclination: uniform -20 380",
                "    xi_period: uniform " + str(3 / 4 * xi_P) + " " + str(4 / 3 * xi_P),
                "    xi_semimajor_axis: log-uniform 0.001 0.1",
                "    xi_argument_of_latitude_reference: uniform -20 380",
                # parallax
                "model:",
                "   coords: " + right_ascension[indeks] + " " + declination[indeks],
                "fixed_parameters:",
                "    t_0_par: 245" + str(t0par),
                "    t_0_xi: 245" + str(t0par),
                "min_values:",
                ("    u_0: 0." if sign == "+" else ""),
                "    t_E: 0.",
                "    xi_semimajor_axis: 0.",
                "    xi_period: 0.",
                "    xi_Omega_node: -20.",
                "    xi_inclination: -20.",
                "    xi_argument_of_latitude_reference: -20.",
                "    pi_E_N: -1.",
                "    pi_E_E: -1.",
                "max_values:",
                "    xi_Omega_node: 380.",
                "    xi_inclination: 380.",
                "    xi_argument_of_latitude_reference: 380.",
                ("    u_0: 0." if sign == "-" else ""),
                "    pi_E_N: 1.",
                "    pi_E_E: 1.",
                "fitting_parameters:",
                "    n_steps: 400",
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
                yaml.writelines(line + "\n")
