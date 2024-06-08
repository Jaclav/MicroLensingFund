import os
import random as r
import sys
import numpy as np
from astropy.coordinates import SkyCoord
from pathlib import Path
import pandas as pd

from microlensing_black_holes.parsubs import velocity_of_Earth_projected

def convert_ra_dec_to_galactic(ra, dec):
    c = SkyCoord(ra, dec, frame='icrs', unit='deg')
    l = c.galactic.l.deg
    b = c.galactic.b.deg
    return l, b
def dms_to_dd(dms_str):
    parts = dms_str.split(":")
    dd = float(parts[0]) + float(parts[1])/60 + float(parts[2])/(60*60)
    return dd

os.mkdir( sys.argv[1] + "/galaxymodel")
os.mkdir(sys.argv[1] + "/galaxymodel/png")


dat = pd.read_csv(
    "./"+sys.argv[1] + "/chi2_with_paraxall.csv", delimiter=",", dtype=str, header=None
)
for i in range(0, 9):
    dat[i].pop(0)

name = dat[0]
better = dat[1]
parallaxPath = dat[3]
xallarapPath = dat[5]
pathParaxall = dat[8]

listFiles = []
listNames = []
for i in range(1, len(name)+1):
    if better[i] == "xallarap":
        listFiles.append(pathParaxall[i])
        listNames.append(pathParaxall[i][15:])
    else:
         listFiles.append(np.nan)
         listNames.append(np.nan)


(name, right_ascension, declination) = np.loadtxt(
    "parallaxData/coords.csv", unpack=True, delimiter=",", dtype=str
)
right_ascension = list(map(dms_to_dd, right_ascension))
declination = list(map(dms_to_dd, declination))

(mu_E_source, mu_E_err_source,mu_N_source, mu_N_err_source, pm_corr_source) = np.loadtxt(
       "parallaxData/proper_motions.csv", unpack=True, delimiter=",", dtype=str
) 


for index, file in enumerate(listNames):
    if type(listFiles[index]) == str:
        (l, b) = convert_ra_dec_to_galactic(right_ascension[index], declination[index])
        f = open(listFiles[index],"r")
        lines = f.readlines()
        for line in lines:
            if "t_0" in line and "u_0" in line:
                    pass    
            elif "t_0" in line:
                    t0 = float(line.split()[2]) - 2450000
                    t0_err = max(float(line.split()[3]), - float(line.split()[4]))
            elif "u_0" in line:
                    u0 = float(line.split()[2])
                    u0_err = max(float(line.split()[3]), - float(line.split()[4]))
            elif "t_E" in line:
                    tE = float(line.split()[2])
                    tE_err = max(float(line.split()[3]), - float(line.split()[4]))
            elif "pi_E_N" in line:
                    piEN = float(line.split()[2])
                    piEN_err = max(float(line.split()[3]), - float(line.split()[4])) 
            elif "pi_E_E" in line:
                    piEE = float(line.split()[2])
                    piEE_err = max(float(line.split()[3]), - float(line.split()[4])) 

        yamlN = Path("./"+sys.argv[1] + "/galaxymodel/" + file + ".yaml")
        print(yamlN)

        yaml = open(yamlN, 'w+')
        t0par = round(t0, -1)
        v_Earth_perp_N, v_Earth_perp_E =velocity_of_Earth_projected(
    t0+2450000, right_ascension[index], declination[index])
        
        YAML = [
        "photfile : " + "dataPoleski/" + file,
        "alpha : " + str(right_ascension[index]),
        "delta : " + str(declination[index]),
        "t0_par : " + str(t0par),
        "l : " + str(l),
        "b : " + str(b),
        "vN : " + str(v_Earth_perp_N),
        "vE : " + str(v_Earth_perp_E),
        "mu_min : " + "0",
        "mu_max : " + "20",
        "mu_E_source : " + str(mu_E_source[index]),
        "mu_N_source : " + str(mu_N_source[index]),
        "mu_E_err_source : " + str(mu_E_err_source[index]),
        "mu_N_err_source : " + str(mu_N_err_source[index]),
        "pm_corr_source : " + str(pm_corr_source[index]),
        "output : " + "/galaxymodel/" + str(file),
        "nwalkers : " + "32",
        "nburnin : " + "1000",
        "nsamples : " + "4000",
        "t0 : " + str(t0),
        "tE : " + str(tE),
        "u0 : " + str(u0),
        "piEN : " + str(piEN),
        "piEE : " + str(piEE),
        "sigma_t0 : " + str(t0_err),
        "sigma_tE : " + str(tE_err),
        "sigma_u0 : " + str(u0_err),
        "sigma_piEN : " + str(piEN_err),
        "sigma_piEE : " + str(piEE_err),
        ]
        for line in YAML:
            yaml.writelines(line + "\n")
