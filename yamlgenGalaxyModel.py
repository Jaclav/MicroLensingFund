import os
import random as r
import sys
import numpy as np
from astropy import units as u
from astropy.coordinates import SkyCoord

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


(name, right_ascension, declination) = np.loadtxt(
    "parallaxData/coords.csv", unpack=True, delimiter=",", dtype=str
)
right_ascension = dms_to_dd(right_ascension)
declination = dms_to_dd(declination)

(mu_E_source, mu_E_err_source,mu_N_source, mu_N_err_source, pm_corr_source) = np.loadtxt(
       "parallaxData/proper_motions.csv", unpack=True, delimeter=",", dtype=str
)

(l, b) = convert_ra_dec_to_galactic(right_ascension, declination)


os.mkdir("../" + sys.argv[1] + "/<galaxymodel")
os.mkdir("../" +sys.argv[1] + "/galaxymodel/png")
os.chdir("../" + sys.argv[1] + "/<paraxall")
listFiles = os.listdir()


for index, file in enumerate(listFiles):
    f = open(listFiles[file],"r")
    lines = f.readlines
    for line in lines:
        if "t_0" and "u_0" in line:
                pass    
        elif "t_0" in line:
                t0 = float(line.split()[1]) - 2450000
                t0_err = max(float(line.split()[2]), - float(line.split()[3])) 
        elif "u_0" in line:
                u0 = float(line.split()[1])
                u0_err = max(float(line.split()[2]), - float(line.split()[3])) 
        elif "t_E" in line:
                tE = float(line.split()[1])
                tE_err = max(float(line.split()[2]), - float(line.split()[3])) 
        elif "pi_E_N" in line:
                piEN = float(line.split()[1])
                piEN_err = max(float(line.split()[2]), - float(line.split()[3])) 
        elif "pi_E_E" in line:
                piEE = float(line.split()[1])
                piEE_err = max(float(line.split()[2]), - float(line.split()[3])) 


        yamlN = "../" + sys.argv[1] + "/galaxymodel/" + file + ".yaml"
        yaml = open(yamlN, "w+")
        t0par = round(t0, -1)
        v_Earth_perp_N, v_Earth_perp_E =velocity_of_Earth_projected(
    t0, right_ascension[index], declination[index])
        
        YAML = [
            "photfile : " + "dataPoleski/" + file,
            "alpha : " + str(right_ascension[index]),
            "delta : " + str(declination[index]),
            "t0_par : " + str(t0par),
            "l : " + str(l[index]),
            "b : " + str(b[index]),
            "vN : " + str(v_Earth_perp_N),
            "vE : " + v_Earth_perp_E,
            "mu_min : " + "0",
            "mu_max : " + "20",
            "mu_E_source : " + str(mu_E_source),
            "mu_N_source : " + str(mu_N_source),
            "mu_E_err_source : " + str(mu_E_err_source),
            "mu_N_err_source : " + str(mu_N_err_source),
            "pm_corr_source : " + str(pm_corr_source),
            "output : " + "/galaxymodel/" + file,
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
