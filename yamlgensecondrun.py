import os
import random as r
import sys
import numpy as np
(name, right_ascension, declination) = np.loadtxt(
    "parallaxData/coords.csv", unpack=True, delimiter=",", dtype=str
)
indeks = -1

os.mkdir(sys.argv[1])
os.mkdir(sys.argv[1] + "/bestmodel")
os.mkdir(sys.argv[1] + "/bestmodel/png")
os.chdir("..")
import random as r
import sys
import numpy as np
(name, right_ascension, declination) = np.loadtxt(
    "parallaxData/coords.csv", unpack=True, delimiter=",", dtype=str
)
indeks = -1

os.mkdir(sys.argv[1])
os.mkdir(sys.argv[1] + "/bestmodel")
os.mkdir(sys.argv[1] + "/bestmodel/png")
os.chdir("..")
YAML = []
names = []
yaml_list = {"yaml_parallax-":0,"yaml_parallax_+":0,"yaml_xallarap":0}

with open("sim27_12chitable.csv", "r") as file:
    lines = file.readlines()
for i in lines:
    words = lines.split(",")
    names.append(words[-1])

for file in names:
    yamlN = "../" + sys.argv[1] + "/bestmodel/" + file + ".yaml"
    parN = "../" + sys.argv[1] + "/bestmodel/" + file + ".par"
yaml = open(yamlN, "w+")

with open("sim27_12chitable.csv", "r") as file:
    lines = file.readlines()
for i in range(len(names)):
    f = open(names[i],"r")
    lines = f.readlines
    for line in lines:
        if "t_0" and "u_0" in line:
                pass    
        elif "t_0" in line:
                t0 = float(line.split()[1])   
        elif "u_0" in line:
                u0 = float(line.split()[1])
        elif "t_E" in line:
                tE = float(line.split()[1])
        elif "xi_period":
             xi_p = line
        t0par = round(t0, -1)
with open("sim27_12chitable.csv", "r") as file:
    lines = file.readlines()   
#parallax-             
for i in lines:
    words = lines.split(",")
if words[-2] == "parallax-":
        t0par = round(t0, -1)

        YAML = [
            "photometry_files:",
            "    dataPoleski/" + file,
            "starting_parameters:",
            "    t_0: gauss 245" + str(t0) + " 0.1",
            "    u_0: gauss " + "-"  +str(u0) + " " + str(0.3 * u0),
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
           # ("    u_0: 0." if sign == "+" else ""),
            "    t_E: 0.",
            "max_values:",
            "    u_0: 0." + "-",
            "fitting_parameters:",
            "    n_steps: 50000",
            "    n_walkers: 20",
            #"plots:",
            #"    best model:",
            #"        file: " + graphicF + ".png",
            #"    trajectory:",
            #"        file: " + graphicF + ".trj.png",
            #"    triangle:",
            #"        file: " + graphicF + ".trg.png",
            #"    trace:",
            #"        file: " + graphicF + ".tra.png",
        ]
        for line in YAML:
            yaml.writelines(line + "\n")
#for parralax+

elif words[-2] == "parallax+":
        t0par = round(t0, -1)

        YAML = [
            "photometry_files:",
            "    dataPoleski/" + file,
            "starting_parameters:",
            "    t_0: gauss 245" + str(t0) + " 0.1",
            "    u_0: gauss " + "+"  +str(u0) + " " + str(0.3 * u0),
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
           # ("    u_0: 0." if sign == "+" else ""),
            "    t_E: 0.",
            "max_values:",
            "    u_0: 0." + "-",
            "fitting_parameters:",
            "    n_steps: 50000",
            "    n_walkers: 20",
            #"plots:",
            #"    best model:",
            #"        file: " + graphicF + ".png",
            #"    trajectory:",
            #"        file: " + graphicF + ".trj.png",
            #"    triangle:",
            #"        file: " + graphicF + ".trg.png",
            #"    trace:",
            #"        file: " + graphicF + ".tra.png",
        ]
        for line in YAML:
            yaml.writelines(line + "\n")
#for xallarap
elif words[-2] == "xallarap":
    YAML = [
            "photometry_files:",
            "    dataPoleski/" + file,
            "starting_parameters:",
            "    t_0: gauss 245" + str(t0) + " 0.1",
            "    u_0: gauss " + str(u0) + " " + str(0.3 * u0),
            "    t_E: gauss " + str(tE) + " " + str(tE * 0.5),
            # parallax
            # "    pi_E_N: uniform -1.0 1.0",
            # "    pi_E_E: uniform -1.0 1.0",
            # xallarap https://doi.org/10.3847/1538-3881/ad284f
            "    xi_Omega_node: uniform -20 380",
            "    xi_inclination: uniform -20 380",
            xi_p,
            "    xi_semimajor_axis: log-uniform 0.001 0.1",
            "    xi_argument_of_latitude_reference: uniform -20 380",
            # parallax
            "model:",
            "   coords: " + right_ascension[indeks] + " " + declination[indeks],
            "fixed_parameters:",
            # "    t_0_par: 245" + str(t0par),
            "    t_0_xi: 245" + str(t0par),
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
            "plots:",
            "    best model:",
            #"        file: " + graphicF + ".png",
            #"        time range: 245" + str(tmin) + " 245" + str(tmax),
            #"    trajectory:",
            #"        file: " + graphicF + ".trj.png",
            #"        time range: 245" + str(tmin) + " 245" + str(tmax),
            #"    triangle:",
            #"        file: " + graphicF + ".trg.png",
            #"    trace:",
            #"        file: " + graphicF + ".tra.png",
        ]
    for line in YAML:
        yaml.writelines(line + "\n")





YAML = []
names = []
yaml_list = {"yaml_parallax-":0,"yaml_parallax_+":0,"yaml_xallarap":0}

with open("sim27_12chitable.csv", "r") as file:
    lines = file.readlines()
for i in lines:
    words = lines.split(",")
    names.append(words[-1])

for file in names:
    yamlN = "../" + sys.argv[1] + "/bestmodel/" + file + ".yaml"
    parN = "../" + sys.argv[1] + "/bestmodel/" + file + ".par"
yaml = open(yamlN, "w+")

with open("sim27_12chitable.csv", "r") as file:
    lines = file.readlines()
for i in range(len(names)):
    f = open(names[i],"r")
    lines = f.readlines
    for line in lines:
        if "t_0" and "u_0" in line:
                pass    
        elif "t_0" in line:
                t0 = float(line.split()[1])   
        elif "u_0" in line:
                u0 = float(line.split()[1])
        elif "t_E" in line:
                tE = float(line.split()[1])
        elif "xi_period":
             xi_p = line
        t0par = round(t0, -1)
with open("sim27_12chitable.csv", "r") as file:
    lines = file.readlines()   
#parallax-             
for i in lines:
    words = lines.split(",")
if words[-2] == "parallax-":
        t0par = round(t0, -1)

        YAML = [
            "photometry_files:",
            "    dataPoleski/" + file,
            "starting_parameters:",
            "    t_0: gauss 245" + str(t0) + " 0.1",
            "    u_0: gauss " + "-"  +str(u0) + " " + str(0.3 * u0),
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
           # ("    u_0: 0." if sign == "+" else ""),
            "    t_E: 0.",
            "max_values:",
            "    u_0: 0." + "-",
            "fitting_parameters:",
            "    n_steps: 50000",
            "    n_walkers: 20",
            #"plots:",
            #"    best model:",
            #"        file: " + graphicF + ".png",
            #"        time range: 245" + str(tmin) + " 245" + str(tmax),
            #"    trajectory:",
            #"        file: " + graphicF + ".trj.png",
            #"        time range: 245" + str(tmin) + " 245" + str(tmax),
            #"    triangle:",
            #"        file: " + graphicF + ".trg.png",
            #"    trace:",
            #"        file: " + graphicF + ".tra.png",
        ]
        for line in YAML:
            yaml.writelines(line + "\n")
#for parralax+

elif words[-2] == "parallax+":
        t0par = round(t0, -1)

        YAML = [
            "photometry_files:",
            "    dataPoleski/" + file,
            "starting_parameters:",
            "    t_0: gauss 245" + str(t0) + " 0.1",
            "    u_0: gauss " + "+"  +str(u0) + " " + str(0.3 * u0),
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
           # ("    u_0: 0." if sign == "+" else ""),
            "    t_E: 0.",
            "max_values:",
            "    u_0: 0." + "-",
            "fitting_parameters:",
            "    n_steps: 50000",
            "    n_walkers: 20",
            #"plots:",
            #"    best model:",
            #"        file: " + graphicF + ".png",
            #"        time range: 245" + str(tmin) + " 245" + str(tmax),
            #"    trajectory:",
            #"        file: " + graphicF + ".trj.png",
            #"        time range: 245" + str(tmin) + " 245" + str(tmax),
            #"    triangle:",
            #"        file: " + graphicF + ".trg.png",
            #"    trace:",
            #"        file: " + graphicF + ".tra.png",
        ]
        for line in YAML:
            yaml.writelines(line + "\n")
#for xallarap
elif words[-2] == "xallarap":
    YAML = [
            "photometry_files:",
            "    dataPoleski/" + file,
            "starting_parameters:",
            "    t_0: gauss 245" + str(t0) + " 0.1",
            "    u_0: gauss " + str(u0) + " " + str(0.3 * u0),
            "    t_E: gauss " + str(tE) + " " + str(tE * 0.5),
            # parallax
            # "    pi_E_N: uniform -1.0 1.0",
            # "    pi_E_E: uniform -1.0 1.0",
            # xallarap https://doi.org/10.3847/1538-3881/ad284f
            "    xi_Omega_node: uniform -20 380",
            "    xi_inclination: uniform -20 380",
            xi_p,
            "    xi_semimajor_axis: log-uniform 0.001 0.1",
            "    xi_argument_of_latitude_reference: uniform -20 380",
            # parallax
            "model:",
            "   coords: " + right_ascension[indeks] + " " + declination[indeks],
            "fixed_parameters:",
            # "    t_0_par: 245" + str(t0par),
            "    t_0_xi: 245" + str(t0par),
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
            "plots:",
            "    best model:",
            #"        file: " + graphicF + ".png",
            #"        time range: 245" + str(tmin) + " 245" + str(tmax),
            #"    trajectory:",
            #"        file: " + graphicF + ".trj.png",
            #"        time range: 245" + str(tmin) + " 245" + str(tmax),
            #"    triangle:",
            #"        file: " + graphicF + ".trg.png",
            #"    trace:",
            #"        file: " + graphicF + ".tra.png",
        ]
    for line in YAML:
        yaml.writelines(line + "\n")




