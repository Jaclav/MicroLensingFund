import os
import random as r
import sys
import numpy as np

# run: ./yamlgen.sh P1
(name, ascension, declination) = np.loadtxt(
    "parallaxData/coords.csv", unpack=True, delimiter=",", dtype=str
)
indeks = -1
os.mkdir(sys.argv[1] + "/yaml2")
os.mkdir(sys.argv[1] + "/png2")
os.chdir("dataPoleski")
listFiles = os.listdir()
for file in listFiles:
    parN = "../" + sys.argv[1] + "/yaml/" + file + ".par"
    print(parN)
    (t0, u0, tE, A, tmin, tmax) = np.loadtxt(parN)

    listF = os.listdir("../" + sys.argv[1] + "/yaml")
    for f in listF:
        if f[::5] == file[::5] and f[::-3] == ".OUT":
            indeks += 1
            with open(f"{f}") as in_file:
                file = in_file

            for line in file:
                line.readline()
                wyrazy = line.split()
                if wyrazy[0] == "t_0":
                    t0 = float(wyrazy[2])
                elif wyrazy[0] == "u_0":
                    u0 = float(wyrazy[2])
                elif wyrazy[0] == "t_E":
                    tE = float(wyrazy[2])

    for n in range(1, 11):
        newFile = file + "." + str(n)
        yamlN = "../" + sys.argv[1] + "/yaml2/" + newFile + ".yaml"
        yaml = open(yamlN, "w+")
        xi_P = r.gauss((80 ** ((n - 1) / 9)) * 5, 0.001)
        t0par = round(t0, -1)
        graphicF = sys.argv[1] + "/png2/" + newFile
        YAML = [
            "photometry_files:",
            "    dataPoleski/" + file,
            "starting_parameters:",
            "    t_0: gauss 245" + str(t0) + " 0.1",
            "    u_0: gauss " + str(u0) + " " + str(0.3 * u0),
            "    t_E: gauss " + str(tE) + " " + str(tE * 0.5),
            # parallax
            "    pi_E_N: uniform -1.0 1.0",
            "    pi_E_E: uniform -1.0 1.0",
            # xallarap https://doi.org/10.3847/1538-3881/ad284f
            "    xi_Omega_node: uniform -20 380",
            "    xi_inclination: uniform -20 380",
            "    xi_period: uniform " + str(3 / 4 * xi_P) + " " + str(4 / 3 * xi_P),
            "    xi_semimajor_axis: log-uniform 0.001 0.1",
            "    xi_argument_of_latitude_reference: uniform -20 380",
            # parallax
            "model:",
            "   coords: " + ascension[indeks] + " " + declination[indeks],
            "fixed_parameters:",
            "    t_0_par: 245" + str(t0par),
            "    t_0_xi: 245" + str(t0par),
            "min_values:",
            "    u_0: 0.",
            "    t_E: 0.",
            "fitting_parameters:",
            "    n_steps: 10000",
            "    n_walkers: 20",
            "plots:",
            "    best model:",
            "        file: " + graphicF + ".png",
            "        time range: 245" + str(tmin) + " 245" + str(tmax),
            "    trajectory:",
            "        file: " + graphicF + ".trj.png",
            "        time range: 245" + str(tmin) + " 245" + str(tmax),
            "    triangle:",
            "        file: " + graphicF + ".trg.png",
            "    trace:",
            "        file: " + graphicF + ".tra.png",
        ]
        for line in YAML:
            yaml.writelines(line + "\n")
