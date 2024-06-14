import os
import pandas
import MulensModel as mm
import matplotlib.pyplot  as plt
from matplotlib import gridspec
import glob 
import numpy as np

#------- model ---------------#
with open("sim30/nothing/PAR-05-noaver.dat.OUT") as file:
    lines = file.readlines()
    for i in range(0,len(lines) - 1):
        
        if "t_0" in lines[i] and "u_0" in lines[i]:
            print(lines[i])
            at0 = float(lines[i + 1].split()[0])
            au0 = float(lines[i + 1].split()[1])
            atE = float(lines[ i + 1].split()[2])


with open("sim30/paraxall/PAR-05-noaver.dat-.OUT") as file:
    lines = file.readlines()
    for i in range(0,len(lines) - 1):
        
        if "t_0" in lines[i] and "u_0" in lines[i]:
            t0 = float(lines[i + 1].split()[0])
            u0 = float(lines[i + 1].split()[1])
            tE = float(lines[i + 1].split()[2])
            pi_E_N = float(lines[i + 1].split()[3])
            pi_E_E = float(lines[i + 1].split()[4])
            xi_Omega_node = float(lines[i + 1].split()[5])
            xi_inclination = float(lines[i + 1].split()[6])
            xi_period = float(lines[i + 1].split()[7])
            xi_semimajor_axis = float(lines[i + 1].split()[8])
            xi_argument_of_latitude_reference = float(lines[i + 1].split()[9])
            
flux_s = 593.8584358967686
flux_b = 145.34182717368708
(name, ra, dec) = np.loadtxt(
    "parallaxData/coords.csv", unpack=True, delimiter=",", dtype=str
)
coords = str(ra[4]) + " " + str(dec[4])

standard_model = mm.Model({'t_0': at0, 'u_0': au0, 't_E': atE})
paraxall_model = mm.Model({'t_0': t0, 'u_0': u0, 't_E': tE,"pi_E_N":pi_E_N,"pi_E_E":pi_E_E,
                           "xi_Omega_node":xi_Omega_node,"xi_inclination":xi_inclination,"xi_period":xi_period,"xi_semimajor_axis":xi_semimajor_axis,"xi_argument_of_latitude_reference":xi_argument_of_latitude_reference}, coords=coords)

 #----------------------------- dataset ----------------------------------#


data= mm.MulensData(file_name="dataPoleski/PAR-05-noaver.dat",comments=["\\", "|"],plot_properties={
            'color': "black"}
            )

standard_event = mm.Event(datasets=data, model=standard_model)

#Plot the residuals

gs = gridspec.GridSpec(2, 1, height_ratios=[5, 1])
t_1 = 2453200
t_2 = 2453700


plt.figure()
ax11 = plt.subplot(gs[0])
standard_event.plot_data(subtract_2450000=True)
standard_event.plot_model()

plt.show()
