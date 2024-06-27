import os
import sys
import numpy as np

# run: python3 yamlgen.py simulation_file_name
os.mkdir(sys.argv[1] + "/nothing")
os.mkdir(sys.argv[1] + "/nothing/png")
os.chdir("dataPoleski")
listFiles = os.listdir()
for file in listFiles:
    yamlN = "../" + sys.argv[1] + "/nothing/" + file + ".yaml"
    parN = "../" + sys.argv[1] + "/nothing/" + file + ".par"
    parameters = os.system(
        "python3 ../scripts/super_mega_script.py " + file + " 2>/dev/null 1>" + parN
    )
    (t0, u0, tE, A, tmin, tmax) = np.loadtxt(parN)
    yaml = open(yamlN, "w+")
    yaml.writelines("photometry_files:\n")
    yaml.writelines("    dataPoleski/" + file + "\n")
    yaml.writelines("starting_parameters:\n")
    yaml.writelines("    t_0: gauss 245" + str(t0) + " 0.1\n")  # short to long julian
    yaml.writelines("    u_0: gauss " + str(u0) + " " + str(0.3 * u0) + "\n")
    yaml.writelines("    t_E: gauss " + str(tE) + " " + str(tE * 0.5) + "\n")
    yaml.writelines("min_values:\n")
    yaml.writelines("    u_0: 0.\n")
    yaml.writelines("    t_E: 0.\n")
    yaml.writelines("max_values:\n")
    yaml.writelines("    u_0: 2.\n")
    yaml.writelines("fit_constraints:\n")
    yaml.writelines("    negative_blending_flux_sigma_mag: 20.\n")
    yaml.writelines("    prior:\n")
    yaml.writelines("        t_E: Mroz et al. 2017\n")
    yaml.writelines("fitting_parameters:\n")
    yaml.writelines("    n_steps: 10000\n")
    yaml.writelines("    n_walkers: 12\n")
    yaml.writelines("plots:\n")
    yaml.writelines("    best model:\n")
    yaml.writelines("        file: " + sys.argv[1] + "/nothing/png/" + file + ".png\n")
