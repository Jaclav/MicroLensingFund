import os
import random as r
import sys
import numpy as np
import yaml

# run: ./yamlgen.sh P1
os.chdir("dataPoleski")
os.mkdir("../" + sys.argv[1] + "/xallarap_final")
os.mkdir("../" + sys.argv[1] + "/xallarap_final/png")



(name, better, parallax, parallaxPath, xallarap, xallarapPaths, deltaChi) = np.loadtxt(
    "../" + sys.argv[1] + "/chi2.csv", unpack=True, delimiter=",", dtype=str, skiprows=1
)
xallarapName = []
xallarapPath = []
for i in range(len(name)):
    if float(deltaChi[i]) > 0.0:
        xallarapPath.append(xallarapPaths[i])
        xallarapName.append(name[i])
# katalog z xalarap
for i, file in enumerate(xallarapName):
    file_path = f"../{sys.argv[1]}/parallax/{file}-.yaml"
    with open(file_path, "r") as yaml_file:
        yaml_content = yaml.safe_load(yaml_file)
        t_0_par = yaml_content.get("fixed_parameters", {}).get("t_0_par", None)

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
                xi_a_err = 10**(int(np.log10(xi_a))-4)
                xi_period_err = 10**(int(np.log10(xi_period))-4)
                break

        
    yamlN = "../" + sys.argv[1] + "/xallarap_final/" + file + ".yaml"
    yamlN = open(yamlN, "w+")
    graphicF = sys.argv[1] + "/xallarap_final/png/" + file
    YAML = [
        "photometry_files:",
        "    dataPoleski/" + xallarapName[i],
        "starting_parameters:",
        "    t_0: gauss " + str(t0) + " 0.01",
        "    u_0: gauss " + str(u0) + " " + format(u0_err, '.10f'),
        "    t_E: gauss " + str(tE) + " " + "0.01",
        "    xi_period: gauss " + str(xi_period) + " " + format(xi_period_err, '.10f'),
        "    xi_semimajor_axis: gauss " + str(xi_a) + " " + format(xi_a_err, '.10f'),
        "    xi_Omega_node: gauss " + str(xi_Omega) + " 1.0",
        "    xi_inclination: gauss " + str(xi_i) + " 1.0",
        "    xi_argument_of_latitude_reference: gauss " + str(xi_u) + " 1.0",
        "fixed_parameters:",
        "    t_0_xi: " + str(t_0_par),
        "min_values:",
        "    u_0: 0.",
        "    t_E: 0.",
        "    xi_semimajor_axis: 0.",
        "    xi_period: 0.",
        "    xi_Omega_node: -20.",
        "    xi_inclination: -20.",
        "    xi_argument_of_latitude_reference: -20.",
        "max_values:",
        "    xi_Omega_node: 380.",
        "    xi_inclination: 380.",
        "    xi_argument_of_latitude_reference: 380.",
        "fitting_parameters:",
        "    n_steps: 50000",
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
        yamlN.writelines(str(line) + "\n")




