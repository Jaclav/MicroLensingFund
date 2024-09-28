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

os.mkdir( sys.argv[1] + "/galaxymodel_parallax")

(name, right_ascension, declination) = np.loadtxt(
    "parallaxData/coords.csv",
    unpack=True,
    delimiter=",",
    dtype=str,
)

(name, better, parallax, parallaxpath, xallarap, xallarapPaths, deltaChi) = np.loadtxt(
    sys.argv[1] + "/chi2.csv", unpack=True, delimiter=",", dtype=str, skiprows=1
)

PM = np.loadtxt(
       "parallaxData/proper_motions.csv", unpack=True, delimiter=",", dtype=float, skiprows=1
) 

ParallaxName = []
ParallaxPath = []
ParallaxYaml = []
RA = []
DEC = []
ProperMotion = []
for i in range(len(name)):
    if float(deltaChi[i]) > 0.0:
        ParallaxPath.append('sim_PAR/parallax_final/' + name[i] + '.OUT')
        ParallaxYaml.append('sim_PAR/parallax_final/' + name[i] + '.yaml')
        ParallaxName.append(name[i])
        RA.append(right_ascension[i])
        DEC.append(declination[i])
        ProperMotion.append(PM[:,i])

ProperMotion = np.array(ProperMotion).T
mu_E_source, mu_E_err_source, mu_N_source, mu_N_err_source, pm_corr_source = ProperMotion[:5,:]


RA = list(map(dms_to_dd, RA))
DEC = list(map(dms_to_dd, DEC))



for index, file in enumerate(ParallaxName):
        (l, b) = convert_ra_dec_to_galactic(RA[index], DEC[index])
        f = open(ParallaxPath[index],"r")
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
        f.close()

        f = open(ParallaxYaml[index],"r")
        lines = f.readlines()
        for line in lines:
            if "t_0_par" in line:
                t0par = float(line.split()[1]) - 2450000
                break
        f.close()

        yamlN = sys.argv[1] + "/galaxymodel_parallax/" + file + ".yaml"
        print(yamlN)


        yaml = open(yamlN, 'w+')
        v_Earth_perp_N, v_Earth_perp_E =velocity_of_Earth_projected(
    t0+2450000, RA[index], DEC[index])
        
        YAML = [
        "photfile : " + "dataPoleski/" + file,
        "alpha : " + str(RA[index]),
        "delta : " + str(DEC[index]),
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
        "output : " + sys.argv[1] + "/galaxymodel_parallax" + str(file),
        "nwalkers : " + "32",
        "nburnin : " + "10000",
        "nsamples : " + "40000",
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
