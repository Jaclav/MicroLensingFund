import os
import random as r
import sys
import numpy as np

os.chdir("dataPoleski")
(name, right_ascension, declination) = np.loadtxt(
    "../" + "/parallaxData/coords.csv",
    unpack=True,
    delimiter=",",
    dtype=str,
)
os.mkdir("../" + sys.argv[1] + "/paraxall")
os.mkdir("../" + sys.argv[1] + "/paraxall/png")

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
        param_vals = lines[14]
        param_vals_list = param_vals.split()
        t0 = float(param_vals_list[0])
        u0 = float(param_vals_list[1])
        tE = float(param_vals_list[2])
        xi_period = float(param_vals_list[3])
        xi_semimajor_axis = float(param_vals_list[4])
        xi_omega_node = float(param_vals_list[5])
        xi_inclination = float(param_vals_list[6])
        xi_argument_of_latitude_reference = float(param_vals_list[7])
        


        u0_err = 10**(int(np.log10(abs(u0)))-4)

        newFile = xallarapName[i]
        yamlN = "../" + sys.argv[1] + "/paraxall/" + newFile + ".yaml"
        yaml = open(yamlN, "w+")
        t0par = round(t0, -1)
        graphicF = sys.argv[1] + "/paraxall/png/" + newFile

        YAML = [
            "photometry_files:",
            "    dataPoleski/" + xallarapName[i],
            "starting_parameters:",
            "    t_0: gauss " + str(t0) + " 0.01",
            "    u_0: gauss " + str(u0) + " " + str(u0_err),
            "    t_E: gauss " + str(tE) + " 0.01",
            # parallax piE=sqrt(PiN^2+pIEE^2)
            "    pi_E_N: gauss 0.00 0.01",
            "    pi_E_E: gauss 0.00 0.01",
            # PARAXALL https://doi.org/10.3847/1538-3881/ad284f
            "    xi_Omega_node: uniform -20 380",
            "    xi_inclination: uniform -20 380",
            "    xi_period: uniform "
            + str(3 / 4 * xi_period)
            + " "
            + str(4 / 3 * xi_period),
            "    xi_semimajor_axis: log-uniform 0.001 0.1",
            "    xi_argument_of_latitude_reference: uniform -20 380",
            # parallax
            "model:",
            "   coords: " + right_ascension[i] + " " + declination[i],
            "fixed_parameters:",
            "    t_0_par: " + str(t0par),
            "    t_0_xi: " + str(t0par),
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
