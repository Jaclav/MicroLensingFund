import os
import random as r
import sys
import numpy as np

# run: ./yamlgen.sh P1
(name, ascension, declination) = np.loadtxt(
    "Coords/coords.csv", unpack=True, delimiter=",", dtype=str
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
    t0par = round(t0, -1)
    for n in range(1, 11):
        newFile = file + "." + str(n)
        yamlN = "../" + sys.argv[1] + "/yaml2/" + newFile + ".yaml"
        yaml = open(yamlN, "w+")
        yaml.writelines("photometry_files:\n")
        yaml.writelines("    dataPoleski/" + file + "\n")
        yaml.writelines("starting_parameters:\n")
        yaml.writelines("    t_0: gauss 245" + str(t0) + " 0.1\n")
        yaml.writelines("    u_0: gauss " + str(u0) + " " + str(0.3 * u0) + "\n")
        yaml.writelines("    t_E: gauss " + str(tE) + " " + str(tE * 0.5) + "\n")

        # parallax
        yaml.writelines("    pi_E_N: uniform " + str(-1.0) + " " + str(1.0) + "\n")
        yaml.writelines("    pi_E_E: uniform " + str(-1.0) + " " + str(1.0) + "\n")

        # xallarap https://doi.org/10.3847/1538-3881/ad284f
        yaml.writelines("    xi_Omega_node: uniform -20 380\n")
        yaml.writelines("    xi_inclination: uniform -20 380\n")
        xi_period = r.gauss((90 ** (n / 9)) * 5, 0.001)
        yaml.writelines(
            "    xi_period: range "
            + str(3 / 4 * xi_period)
            + " "
            + str(4 / 3 * xi_period)
            + "\n"
        )
        yaml.writelines("    xi_semimajor_axis: log-uniform 0.001 0.1\n")
        yaml.writelines("    xi_argument_of_latitude_reference: uniform -20 380\n")

        # parallax
        yaml.writelines("model:\n")
        yaml.writelines(
            "   coords: " + ascension[indeks] + " " + declination[indeks] + "\n"
        )

        yaml.writelines("fixed_parameters:\n")
        yaml.writelines("    t_0_par: 245" + str(t0par) + "\n")
        yaml.writelines("    t_0_xi: 245" + str(t0par) + "\n")
        yaml.writelines("min_values:\n")
        yaml.writelines("    u_0: 0.\n")
        yaml.writelines("    t_E: 0.\n")
        yaml.writelines("fitting_parameters:\n")
        yaml.writelines("    n_steps: 10000\n")
        yaml.writelines("    n_walkers: 20\n")
        yaml.writelines("plots:\n")
        yaml.writelines("    best model:\n")
        yaml.writelines("        file: " + sys.argv[1] + "/png2/" + newFile + ".png\n")
        yaml.writelines(
            "        time range: 245" + str(tmin) + " 245" + str(tmax) + "\n"
        )
        yaml.writelines("    trajectory:\n")
        yaml.writelines(
            "        file: " + sys.argv[1] + "/png2/" + newFile + ".trj.png\n"
        )
        yaml.writelines(
            "        time range: 245" + str(tmin) + " 245" + str(tmax) + "\n"
        )
        yaml.writelines("    triangle:\n")
        yaml.writelines(
            "        file: " + sys.argv[1] + "/png2/" + newFile + ".trg.png\n"
        )
        yaml.writelines("    trace:\n")
        yaml.writelines(
            "        file: " + sys.argv[1] + "/png2/" + newFile + ".tra.png\n"
        )
