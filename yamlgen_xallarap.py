import os
import random as r
import sys
import numpy as np
import yaml

# run: python3 yamlgen_xallarap.py DirName
os.mkdir(sys.argv[1] + "/xallarap")
os.mkdir(sys.argv[1] + "/xallarap/png")
os.chdir("dataPoleski")
listFiles = os.listdir()

for index, file in enumerate(listFiles):

    file_path = f"../{sys.argv[1]}/parallax/{file}-.yaml"
    with open(file_path, "r") as yaml_file:
        yaml_content = yaml.safe_load(yaml_file)
        t_0_par = yaml_content.get("fixed_parameters", {}).get("t_0_par", None)


    fileOUTm = open("../" + sys.argv[1] + "/parallax/" + file + "-" + ".OUT", "r") 
    fileOUTp = open("../" + sys.argv[1] + "/parallax/" + file + "+" + ".OUT", "r")
    linesm = fileOUTm.readlines()
    linesp = fileOUTp.readlines()

    chim = linesm[:][12]
    chim = float(chim.split()[1])
    chip = linesp[:][12]
    chip = float(chip.split()[1])

    if chim < chip:
        lines = linesm
    else:
        lines = linesp


    print("../" + sys.argv[1] + "/parallax/" + file + ".OUT")

    param_vals = lines[:][14]
    param_vals_list = param_vals.split()
    t0 = float(param_vals_list[0])
    u0 = float(param_vals_list[1])
    tE = float(param_vals_list[2])

    u0_err = 10**(int(np.log10(abs(u0)))-2)
        
    for n in range(1, 11):
        newFile = file + "." + str(n)
        yamlN = "../" + sys.argv[1] + "/xallarap/" + newFile + ".yaml"
        yamlN = open(yamlN, "w+")
        xi_P = r.gauss((80 ** ((n - 1) / 9)) * 5, 0.001)
        graphicF = sys.argv[1] + "/xallarap/png/" + newFile
        if u0 > 0:
            YAML = [
                "photometry_files:",
                "    dataPoleski/" + file,
                "starting_parameters:",
                "    t_0: gauss " + str(t0) + " 0.01",
                "    u_0: gauss " + str(u0) + " " + format(u0_err, '.10f'),
                "    t_E: gauss " + str(tE) + " " + " 0.01",
                # xallarap https://doi.org/10.3847/1538-3881/ad284f
                "    xi_Omega_node: uniform -20 380",
                "    xi_inclination: uniform -20 380",
                "    xi_period: uniform " + str(3 / 4 * xi_P) + " " + str(4 / 3 * xi_P),
                "    xi_semimajor_axis: log-uniform 0.001 0.1",
                "    xi_argument_of_latitude_reference: uniform -20 380",
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
                "    n_steps: 800",
                "    n_walkers: 1000",
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
        else:
                        YAML = [
                "photometry_files:",
                "    dataPoleski/" + file,
                "starting_parameters:",
                "    t_0: gauss " + str(t0) + " 0.01",
                "    u_0: gauss " + str(u0) + " " + format(u0_err, '.10f'),
                "    t_E: gauss " + str(tE) + " " + " 0.01",
                # xallarap https://doi.org/10.3847/1538-3881/ad284f
                "    xi_Omega_node: uniform -20 380",
                "    xi_inclination: uniform -20 380",
                "    xi_period: uniform " + str(3 / 4 * xi_P) + " " + str(4 / 3 * xi_P),
                "    xi_semimajor_axis: log-uniform 0.001 0.1",
                "    xi_argument_of_latitude_reference: uniform -20 380",
                "fixed_parameters:",
                "    t_0_xi: " + str(t_0_par),
                "min_values:",
                "    t_E: 0.",
                "    xi_semimajor_axis: 0.",
                "    xi_period: 0.",
                "    xi_Omega_node: -20.",
                "    xi_inclination: -20.",
                "    xi_argument_of_latitude_reference: -20.",
                "max_values:",
                "    u_0: 0.",
                "    xi_Omega_node: 380.",
                "    xi_inclination: 380.",
                "    xi_argument_of_latitude_reference: 380.",
                "fitting_parameters:",
                "    n_steps: 800",
                "    n_walkers: 1000",
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
            yamlN.writelines(line + "\n")
