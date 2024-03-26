import os
import sys
import numpy as np

# run: ./yamlgen.sh P1
os.mkdir(sys.argv[1])
os.mkdir(sys.argv[1] + "/yaml")
os.mkdir(sys.argv[1] + "/png")
os.chdir("dataPoleski")
listFiles = os.listdir()
for file in listFiles:
    yamlN = "../" + sys.argv[1] + "/yaml/" + file + ".yaml"
    parN = "../" + sys.argv[1] + "/yaml/" + file + ".par"
    parameters = os.system(
        "python3 ../scripts/super_mega_script.py " + file + " 2>/dev/null 1>" + parN
    )
    (t0, u0, tE, A, tmin, tmax) = np.loadtxt(parN)
    yaml = open(yamlN, "w+")
    yaml.writelines("photometry_files:\n")
    yaml.writelines("    dataPoleski/" + file + "\n")
    yaml.writelines("starting_parameters:\n")
    yaml.writelines(
        "    t_0: gauss 245" + str(t0) + "0 0.1\n"
    )  # short Julian to long Julian
    yaml.writelines(
        "    u_0: gauss " + str(u0) + " " + str(0.3 * u0) + "\n"
    )  # TODO: add uncertanity
    yaml.writelines("    t_E: gauss " + str(tE) + " " + str(tE * 0.5) + "\n")
    yaml.writelines("min_values:\n")
    yaml.writelines("    u_0: 0.\n")
    yaml.writelines("    t_E: 0.\n")
    yaml.writelines("fitting_parameters:\n")
    yaml.writelines("    n_steps: 10000\n")
    yaml.writelines("plots:\n")
    yaml.writelines("    best model:\n")
    yaml.writelines("        file: " + sys.argv[1] + "/png/" + file + ".png\n")
    yaml.writelines("        time range: 245" + str(tmin) + " 245" + str(tmax) + "\n")
