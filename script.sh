#!/bin/bash
mkdir $1
mkdir $1/yaml
mkdir $1/png
cd dataPoleski
ls | while read f;
do
	t=`head $f -n 1 | awk -F ' ' '{print $1}'` # t_0
	file=../$1/yaml/$f.yaml
	echo "photometry_files:" > $file
	echo "    $f" >> $file
	echo "starting_parameters:" >> $file
	echo "    t_0: gauss $t 0.1" >> $file
	echo "    u_0: uniform 0.001 1." >> $file
	echo "    t_E: gauss 20. 5." >> $file
	echo "min_values:" >> $file
	echo "    u_0: 0." >> $file
	echo "    t_E: 0." >> $file
	echo "fitting_parameters:" >> $file
	echo "    n_steps: 5000" >> $file
	echo "plots:" >> $file
	echo "    best model:" >> $file
	echo "        file: ../$1/png/$f.png" >> $file
	#python3 ../ulens_model_fit.py moje.yaml
done
