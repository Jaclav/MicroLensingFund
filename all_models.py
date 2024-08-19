import yaml
from tabulate import tabulate
import pandas
import re

#this script reads the output files of the models and stores the values of the fitted parameters in a table

# List of files
files = [r'sim_GAIA/parallax/Gaia19dke_phot_public.dat-.OUT', r'sim_GAIA/xallarap_final/Gaia19dke_phot_public.dat.OUT', r'sim_GAIA/1L2S_xallarap_final/Gaia19dke_phot_public.dat.OUT']
new_files = [f'{file}.yaml' for file in files]

# Cut the files after the line containing "chi2"
new_lines = []
for file in files:
    with open(file, 'r') as f:
        lines = f.readlines()
    for line in lines:
        new_lines.append(line)
        new_file = f'{file}.yaml'
        with open(new_file, 'w') as f:
            f.writelines(new_lines)
        if 'chi2' in line:
            break

# Write the modified lines to a new file


# Read YAML files and store their contents
data = []
for file in new_files:
    with open(file, 'r') as f:
        content = yaml.load(f, Loader=yaml.FullLoader)
        # fitted_parameters = content["Fitted parameters"]
        data.append(content)

grouped_data = {}
for d in data:
    for key, value in d.items():
        if key in grouped_data:
            grouped_data[key].append(value)
        else:
            grouped_data[key] = [value]

table = pandas.DataFrame(data).transpose()
table.columns = [ 'parallax', 'xallarap', '1L2S xallarap']
table = table.to_latex(escape=False)
print(table)