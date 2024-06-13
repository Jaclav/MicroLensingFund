import os
import pandas
import MulensModel as mm
import matplotlib.pyplot  as plt
from matplotlib import gridspec
import glob 

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

standarf_model = mm.Model({'t_0': at0, 'u_0': au0, 't_E': atE})
paraxall_model = mm.Model({'t_0': t0, 'u_0': u0, 't_E': tE,"pi_E_N":pi_E_N,"pi_E_E":pi_E_E,
                           "xi_Omega_node":xi_Omega_node,"xi_inclination":xi_inclination,"xi_period":xi_period,"xi_semimajor_axis":xi_semimajor_axis,"xi_argument_of_latitude_reference":xi_argument_of_latitude_reference})

 #----------------------------- dataset ----------------------------------#

data_red = mm.MulensData(file_name="dataPoleski/PAR-05-noaver.dat",comments=["\\", "|"],plot_properties={
            'color': "red",
            "s":20}
            )
data_green = mm.MulensData(file_name="dataPoleski/PAR-05-noaver.dat",comments=["\\", "|"],plot_properties={
            'color': "green"}
            )

event_default = mm.Event(datasets=data_red,model=standarf_model)

event_paraxall = mm.Event(datasets=data_green,model=paraxall_model)

gs = gridspec.GridSpec(2, 1, height_ratios=[5, 1])
plt.figure
ax11 = plt.subplot(gs[0])
event_default.plot_model(subtract_2450000=True)
event_default.plot_data(subtract_2450000=True)
plt.title('Data and Fitted Model (Default)')
#Plot the residuals
plt.subplot(gs[1], sharex=ax11)
event_default.plot_residuals(subtract_2450000=True)

gs = gridspec.GridSpec(2, 1, height_ratios=[5, 1])
ax11 = plt.subplot(gs[0])
event_paraxall.plot_model(subtract_2450000=True)
event_paraxall.plot_data(subtract_2450000=True)
#Plot the residuals
plt.subplot(gs[1], sharex=ax11)
event_paraxall.plot_residuals(subtract_2450000=True)





#,"coords": "18:04:48.79 -29:40:31.1"
#plt.figure()
#plt.title('Trajectory w/Data (Default)')
#event_default.plot_trajectory()
#event_default.plot_source_for_datasets()

#event_paraxall.plot_trajectory()
#event_paraxall.plot_source_for_datasets()

#gs = gridspec.GridSpec(2, 1, height_ratios=[5, 1])
#ax31 = plt.subplot(gs[0])
#plt.subplot(gs[1], sharex=ax31)
#event_default.plot_residuals(marker='s', markersize=3, subtract_2450000=True)

#event_paraxall.plot_residuals(marker='s', markersize=3, subtract_2450000=True)

plt.show()
