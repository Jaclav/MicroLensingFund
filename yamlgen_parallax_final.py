import os
import random as r
import sys
import numpy as np
import yaml

os.chdir("dataPoleski")
(name, right_ascension, declination) = np.loadtxt(
    "../" + "/parallaxData/coords.csv",
    unpack=True,
    delimiter=",",
    dtype=str,
)

os.mkdir("../" + sys.argv[1] + "/parallax_final")
os.mkdir("../" + sys.argv[1] + "/parallax_final/png")

(name, better, parallax, parallaxPath, xallarap, xallarapPaths, deltaChi) = np.loadtxt(
    "../" + sys.argv[1] + "/chi2.csv", unpack=True, delimiter=",", dtype=str, skiprows=1
)



ParallaxName = []
ParallaxPath = []
RA = []
DEC = []
for i in range(len(name)):
    if float(deltaChi[i]) > 0.0:
        ParallaxPath.append(parallaxPath[i])
        ParallaxName.append(name[i])
        RA.append(right_ascension[i])
        DEC.append(declination[i])
# katalog z xalarap
for i, file in enumerate(ParallaxName):
    file_path = f"../{sys.argv[1]}/parallax/{file}-.yaml"
    with open(file_path, "r") as yaml_file:
        yaml_content = yaml.safe_load(yaml_file)
        t_0_par = yaml_content.get("fixed_parameters", {}).get("t_0_par", None)

    with open(ParallaxPath[i], "r") as fileOUT:
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
                pi_E_N = float(tab["pi_E_N"])
                pi_E_E = float(tab["pi_E_E"])

                u0_err = 10**(int(np.log10(abs(u0)))-2)
                Pi_E_N_err = 10**(int(np.log10(abs(pi_E_N)))-2)
                Pi_E_E_err = 10**(int(np.log10(abs(pi_E_E)))-2)
                break

        
    yamlN = "../" + sys.argv[1] + "/parallax_final/" + file + ".yaml"
    yamlN = open(yamlN, "w+")
    graphicF = sys.argv[1] + "/parallax_final/png/" + file
    YAML = [
        "photometry_files:",
        "    dataPoleski/" + ParallaxName[i],
        "starting_parameters:",
        "    t_0: gauss " + str(t0) + " 0.01",
        "    u_0: gauss " + str(u0) + " " + format(u0_err, '.10f'),
        "    t_E: gauss " + str(tE) + " " + "0.01",
        "    pi_E_N: gauss " + str(pi_E_N) + " " + format(Pi_E_N_err, '.10f'),
        "    pi_E_E: gauss " + str(pi_E_E) + " " + format(Pi_E_E_err, '.10f'),
        "model:",
        "   coords: " + RA[i] + " " + DEC[i],
        "fixed_parameters:",
        "    t_0_par: " + str(t_0_par),
        "min_values:",
        ("    u_0: 0." if u0>0 else ""),
        "    t_E: 0.",
        "max_values:",
        ("    u_0: 0." if u0<0 else ""),
        "fitting_parameters:",
        "    n_steps: 60000",
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




