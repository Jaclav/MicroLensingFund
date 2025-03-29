import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import find_peaks
from scipy.signal import lombscargle
import MulensModel as mm

# List of event IDs
# event_ids = ["PAR-06", "PAR-14", "PAR-15", "PAR-35", "PAR-39", "PAR-44", "PAR-47", "PAR-52", "PAR-57", "PAR-58", "PAR-59"]
event_ids = ["PAR-44"]

# Iterate over each event
for event_id in event_ids:
    print(f"Processing event: {event_id}")
    
    # Load the .dat file
    data_file = f"dataPoleski/{event_id}-noaver.dat"
    data = np.loadtxt(data_file)
    jd = data[:, 0] + 2450000
    mag = data[:, 1]
    err = data[:, 2]
    
    # Read model parameters from corresponding .OUT file
    with open(f'sim_PAR/nothing/{event_id}-noaver.dat.OUT', 'r') as file:
        lines = file.readlines()
        standard_fluxes = [0, 0]
        for i in range(len(lines) - 1):
            if "t_0" in lines[i] and "u_0" in lines[i]:
                t0 = float(lines[i + 1].split()[0])
                u0 = float(lines[i + 1].split()[1])
                tE = float(lines[i + 1].split()[2])
                standard_fluxes[0] = float(lines[i + 3].split()[0])
                standard_fluxes[1] = float(lines[i + 3].split()[1])
    
    model = mm.Model({'t_0': t0, 'u_0': u0, 't_E': tE})
    
    with open(f'sim_PAR/xallarap_final_2/{event_id}-noaver.dat.OUT','r') as file:
        lines = file.readlines()
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
                # q_source = float(lines[i + 1].split()[8])
    model = mm.Model({'t_0': t0, 'u_0': u0, 't_E': tE, 'xi_period': xi_period, 'xi_semimajor_axis': xi_semimajor_axis,
                                'xi_Omega_node': xi_Omega_node, 'xi_inclination': xi_inclination, 'xi_argument_of_latitude_reference': xi_argument_of_latitude_reference,
                                't_0_xi': 2454314})

    # Create an Event object
    dataset = mm.MulensData(file_name=data_file, add_2450000=True, phot_fmt='mag')
    event = mm.Event(datasets=dataset, model=model)
    
    fit = mm.fitdata.FitData(model=event.model, dataset=dataset)
    fit.fit_fluxes()
    residuals, errorbars = fit.get_residuals(phot_fmt='mag')
    
    # Fourier analysis on residuals
    filtered_jd = jd
    filtered_residuals = residuals
    filtered_mag = mag
    filtered_err = err
    
    # Define frequencies for Lomb-Scargle Periodogram
    min_frequency = 1 / 600  
    max_frequency = 1 / 20  
    frequencies = np.linspace(min_frequency, max_frequency, len(filtered_residuals))
    angular_frequencies = 2 * np.pi * frequencies
    
    # Perform Lomb-Scargle Periodogram
    power = lombscargle(filtered_jd - filtered_jd.min(), filtered_residuals, angular_frequencies)
    
    # Plot the light curve and residuals
    plt.figure(figsize=(12, 6))
    # Subplot 1: Light curve
    plt.subplot(2, 1, 1)
    plt.errorbar(filtered_jd - 2450000, filtered_mag, yerr=filtered_err, fmt='o', label='Data')
    event.plot_model(color='red', zorder=10, label='Model', subtract_2450000=True, t_range=[filtered_jd.min(), filtered_jd.max()])
    plt.xlabel('Julian Date')
    plt.ylabel('Magnitude')
    plt.legend()
    plt.title(f'Light Curve for {event_id}')
    
    # Subplot 2: Residuals
    plt.subplot(2, 1, 2)
    plt.errorbar(jd, residuals, yerr=err, fmt='o')
    plt.axhline(0, color='red', linestyle='--')
    plt.xlabel('Julian Date')
    plt.ylabel('Residuals (mag)')
    plt.title('Residuals')
    
    plt.tight_layout()
    plt.show()
    
    # Plot the Lomb-Scargle Periodogram
    # plt.figure(figsize=(8, 6))
    # plt.plot(frequencies, power, label='Lomb-Scargle Power')
    # plt.xlabel('Frequency (1/day)')
    # plt.ylabel('Power')
    # plt.title(f'Fourier Analysis of Residuals for {event_id}')
    # plt.legend()
    # plt.show()
    
    # Find peaks in the Lomb-Scargle Periodogram
    peaks, _ = find_peaks(power)
    # Get the three highest peaks
    highest_peaks = np.argsort(power[peaks])[-3:]
    peak_frequencies = frequencies[peaks][highest_peaks]
    peak_powers = power[peaks][highest_peaks]
    
    # Print the coordinates of the three biggest peaks
    print(f"Event {event_id}:")
    for i, (freq, power) in enumerate(zip(peak_frequencies, peak_powers)):
        print(f"  Peak {i+1}: Period = {1/freq:.2f}, Power = {power:.4f}")
