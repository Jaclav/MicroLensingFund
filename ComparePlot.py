import os
import pandas
import MulensModel as mm
import matplotlib.pyplot  as plt
from matplotlib import gridspec
import glob 
import numpy as np

#this script compares the residuals of the models analyzed in sim_GAIA
#!!!!!!!!!!!!!!!!WARNING - this script has hardcoded t_0_par and t_0_xi values!!!!!!!!!!!!!!!!

#------- model ---------------#
with open(r'sim_GAIA/nothing/Gaia19dke_phot_public.dat.OUT','r') as file:
    lines = file.readlines()
    standard_fluxes = [0,0]
    for i in range(0,len(lines) - 1):
        
        if "t_0" in lines[i] and "u_0" in lines[i]:
            t0 = float(lines[i + 1].split()[0])
            u0 = float(lines[i + 1].split()[1])
            tE = float(lines[i + 1].split()[2])
            standard_fluxes[0] = float(lines[i + 3].split()[0])
            standard_fluxes[1] = float(lines[i + 3].split()[1])
standard_model = mm.Model({'t_0': t0, 'u_0': u0, 't_E': tE})


with open(r'sim_GAIA/parallax_final/Gaia19dke_phot_public.dat.OUT','r') as file:
    lines = file.readlines()
    parallax_fluxes = [0,0]
    for i in range(0,len(lines) - 1):
        
        if "t_0" in lines[i] and "u_0" in lines[i]:
            t0 = float(lines[i + 1].split()[0])
            u0 = float(lines[i + 1].split()[1])
            tE = float(lines[i + 1].split()[2])
            pi_E_N = float(lines[i + 1].split()[3])
            pi_E_E = float(lines[i + 1].split()[4])
            coords = '19:25:58.68  28:24:24.70'
            parallax_fluxes[0] = float(lines[i + 3].split()[0])
            parallax_fluxes[1] = float(lines[i + 3].split()[1])
parallax_model = mm.Model({'t_0': t0, 'u_0': u0, 't_E': tE, 'pi_E_N': pi_E_N, 'pi_E_E': pi_E_E, 't_0_par': 2459071}, coords=coords)

with open(r'sim_GAIA/1L2S_xallarap_final/Gaia19dke_phot_public.dat.OUT','r') as file:
    lines = file.readlines()
    xallarap_fluxes = [0,0,0]
    for i in range(0,len(lines) - 1):
        
        if "t_0" in lines[i] and "u_0" in lines[i]:
            t0 = float(lines[i + 1].split()[0])
            u0 = float(lines[i + 1].split()[1])
            tE = float(lines[i + 1].split()[2])
            xi_period = float(lines[i + 1].split()[3])
            xi_semimajor_axis = float(lines[i + 1].split()[4])
            xi_Omega_node = float(lines[i + 1].split()[5])
            xi_inclination = float(lines[i + 1].split()[6])
            xi_argument_of_latitude_reference = float(lines[i + 1].split()[7])
            q_source = float(lines[i + 1].split()[8])
            xallarap_fluxes[0] = float(lines[i + 3].split()[0])
            xallarap_fluxes[1] = float(lines[i + 3].split()[1])
            xallarap_fluxes[2] = float(lines[i + 3].split()[2])
xallarap_model = mm.Model({'t_0': t0, 'u_0': u0, 't_E': tE, 'xi_period': xi_period, 'xi_semimajor_axis': xi_semimajor_axis,
                            'xi_Omega_node': xi_Omega_node, 'xi_inclination': xi_inclination, 'xi_argument_of_latitude_reference': xi_argument_of_latitude_reference,
                            'q_source': q_source, 't_0_xi': 2459078})

 #----------------------------- dataset ----------------------------------#


data= mm.MulensData(file_name=r'dataGAIA/Gaia19dke_phot_public.dat',plot_properties={
            'color': "black"}, add_2450000=True)


standard_event = mm.Event(datasets=data, model=standard_model)
parallax_event = mm.Event(datasets=data, model=parallax_model)
xallarap_event = mm.Event(datasets=data, model=xallarap_model)


#Plot the residuals

gs = gridspec.GridSpec(2, 1, hspace=0, height_ratios=(5,1))
t_1 = 2458000
t_2 = 2460000

## standard vs parallax ##
plt.figure()

axes = plt.subplot(gs[0])

standard_event.plot_data(show_errorbars=True, subtract_2450000=True, markersize=3)

# standard_event.plot_model(t_range=[t_1, t_2], subtract_2450000=True)
parallax_event.plot_model(t_range=[t_1, t_2], subtract_2450000=True, color='red')
xallarap_event.plot_model(t_range=[t_1, t_2],subtract_2450000=True, color='tab:blue')

plt.legend(['Parallax','1L2S_xallarap'], loc='upper right')

ax = plt.gca()
ax.get_xaxis().set_visible(False)

plt.xlim(t_1-2450000, t_2-2450000)

axes = plt.subplot(gs[1])

# standard_event.plot_residuals(subtract_2450000=True,markersize=3, show_errorbars=True)
parallax_event.plot_residuals(subtract_2450000=True,markersize=3, show_errorbars=True)
# xallarap_event.plot_residuals(subtract_2450000=True,markersize=3, show_errorbars=True)
plt.ylim(-0.03, 0.03)
plt.gca().invert_yaxis()

t_array = np.linspace(t_1-2450000, t_2-2450000, 1000)
# standard_lc = (t_array, standard_model.get_lc(source_flux=standard_fluxes[0], blend_flux=standard_fluxes[1], t_range=[t_1, t_2]))
parallax_lc = (t_array, parallax_model.get_lc(source_flux=parallax_fluxes[0], blend_flux=parallax_fluxes[1],  t_range=[t_1, t_2]))
xallarap_lc = (t_array, xallarap_model.get_lc(source_flux=[xallarap_fluxes[0],xallarap_fluxes[1]], blend_flux=xallarap_fluxes[2],  t_range=[t_1, t_2]))
# xallarap_lc = (t_array, xallarap_model.get_lc(source_flux=xallarap_fluxes[0], blend_flux=xallarap_fluxes[1],  t_range=[t_1, t_2]))

# residuals = (t_array, parallax_lc[1] - standard_lc[1])
residuals = (t_array, parallax_lc[1] - xallarap_lc[1])

plt.plot(residuals[0], residuals[1], color='tab:blue')
plt.xlim(t_1-2450000, t_2-2450000)

plt.savefig('parallax-1L2S_xallarap.png', dpi=500)
# plt.show()
plt.close()

