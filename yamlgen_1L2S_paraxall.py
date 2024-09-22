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
os.mkdir("../" + sys.argv[1] + "/1L2S_paraxall")
os.mkdir("../" + sys.argv[1] + "/1L2S_paraxall/png")

(name, better, parallax, parallaxPath, xallarap, xallarapPaths, deltaChi) = np.loadtxt(
    "../" + sys.argv[1] + "/chi2.csv", unpack=True, delimiter=",", dtype=str, skiprows=1
)
xallarapName = []
xallarap_circular = []
xallarap_elliptic = []
for i in range(len(name)):
    if float(deltaChi[i]) > 0.0:
        xallarap_circular.append('../sim_PAR/1L2S_xallarap_circular/' + name[i] + '.OUT')
        xallarap_elliptic.append('../sim_PAR/1L2S_xallarap_elliptic/' + name[i] + '.OUT')
        xallarapName.append(name[i])
print(xallarapName)

chi2_circular = []
chi2_elliptic = []
for i in range(len(xallarap_circular)):
    with open(xallarap_circular[i], "r") as file:
        lines = file.readlines()
        for k in range(len(lines)):
            if "chi2" in lines[k]:
                keys = lines[k].split()
                
                chi2_circular.append(float(keys[1]))
                break
for i in range(len(xallarap_elliptic)):
    with open(xallarap_elliptic[i], "r") as file:
        lines = file.readlines()
        for k in range(len(lines)):
            if "chi2" in lines[k]:
                keys = lines[k].split()
                
                chi2_elliptic.append(float(keys[1]))
                break

xallarapPath = []
parallax_path = []
for i in range(len(xallarapName)):
    if chi2_circular[i] < chi2_elliptic[i]:
        xallarapPath.append(xallarap_circular[i])
    else:
        xallarapPath.append(xallarap_elliptic[i])    

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
                q_source = float(tab["q_source"])
                if chi2_elliptic[i] < chi2_circular[i]:
                    xi_e = float(tab["xi_eccentricity"])
                    xi_omega_per = float(tab["xi_omega_periapsis"])                    

                u0_err = 10**(int(np.log10(abs(u0)))-4)
                xi_a_err = 10**(int(np.log10(xi_a))-3)
                xi_period_err = 10**(int(np.log10(xi_period))-2)
                q_source_err = 10**(int(np.log10(q_source))-2)
                break
    with open(parallaxPath[i], "r") as fileOUT:
        lines = fileOUT.readlines()
        for k in range(len(lines)):
            if "t_0" in lines[k] and "u_0" in lines[k]:
                keys = lines[k].split()
                vals = lines[k + 1].split()
                tab = {}
                for j in range(len(keys)):
                    tab[keys[j]] = vals[j]
                piE_N = float(tab["pi_E_N"])
                piE_E = float(tab["pi_E_E"])


    newFile = xallarapName[i]
    yamlN = "../" + sys.argv[1] + "/1L2S_paraxall/" + newFile + ".yaml"
    yaml = open(yamlN, "w+")
    graphicF = sys.argv[1] + "/1L2S_paraxall/png/" + newFile
    if chi2_elliptic[i] < chi2_circular[i]:
        YAML = [
            "photometry_files:",
            "    dataPoleski/" + xallarapName[i],
            "starting_parameters:",
            "    t_0: gauss " + str(t0) + " 0.01",
            "    u_0: gauss " + str(u0) + " " + format(u0_err, '.10f'),
            "    t_E: gauss " + str(tE) + " 0.01",
            # parallax piE=sqrt(PiN^2+pIEE^2)
            "    pi_E_N: gauss " + str(piE_N) + " 0.01",
            "    pi_E_E: gauss " + str(piE_E) + " 0.01",
            # PARAXALL https://doi.org/10.3847/1538-3881/ad284f
            "    xi_Omega_node: gauss " + str(xi_Omega) + " 1.0",
            "    xi_inclination: gauss " + str(xi_i) + " 1.0",
            "    xi_period: gauss " + str(xi_period) + " " + format(xi_period_err, '.10f'),
            "    xi_argument_of_latitude_reference: gauss " + str(xi_u) + " 1.0",
            "    xi_semimajor_axis: gauss " + str(xi_a) + " " + format(xi_a_err, '.10f'),
            "    q_source: gauss " + str(q_source) + " " + format(q_source_err, '.10f'),
            "    xi_eccentricity: gauss " + str(xi_e) + " 0.01",
            "    xi_omega_periapsis: gauss " + str(xi_omega_per) + " 1.0",
            # parallax
            "model:",
            "   coords: " + right_ascension[i] + " " + declination[i],
            "fixed_parameters:",
            "    t_0_par: " + str(round(t0)),
            "    t_0_xi: " + str(round(t0)),
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
            "    q_source: 1.",
            "fitting_parameters:",
            "    n_steps: 50000",
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
    else:
        YAML = [
            "photometry_files:",
            "    dataPoleski/" + xallarapName[i],
            "starting_parameters:",
            "    t_0: gauss " + str(t0) + " 0.01",
            "    u_0: gauss " + str(u0) + " " + format(u0_err, '.10f'),
            "    t_E: gauss " + str(tE) + " 0.01",
            # parallax piE=sqrt(PiN^2+pIEE^2)
            "    pi_E_N: gauss " + str(piE_N) + " 0.01",
            "    pi_E_E: gauss " + str(piE_E) + " 0.01",
            # PARAXALL https://doi.org/10.3847/1538-3881/ad284f
            "    xi_Omega_node: gauss " + str(xi_Omega) + " 1.0",
            "    xi_inclination: gauss " + str(xi_i) + " 1.0",
            "    xi_period: gauss " + str(xi_period) + " " + format(xi_period_err, '.10f'),
            "    xi_argument_of_latitude_reference: gauss " + str(xi_u) + " 1.0",
            "    xi_semimajor_axis: gauss " + str(xi_a) + " " + format(xi_a_err, '.10f'),
            "    q_source: gauss " + str(q_source) + " " + format(q_source_err, '.10f'),
            # parallax
            "model:",
            "   coords: " + right_ascension[i] + " " + declination[i],
            "fixed_parameters:",
            "    t_0_par: " + str(round(t0)),
            "    t_0_xi: " + str(round(t0)),
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
            "max_values:",
            "    xi_Omega_node: 380.",
            "    xi_inclination: 380.",
            "    xi_argument_of_latitude_reference: 380.",
            "    pi_E_N: 1.",
            "    pi_E_E: 1.",
            "    q_source: 1.",
            "fitting_parameters:",
            "    n_steps: 50000",
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
