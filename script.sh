#!/bin/bash
mkdir $1_yaml
mkdir $1_png
cd dataPoleski
ls | while read f;
do
	t=`head $f -n 1 | awk -F ' ' '{print $1}'` # t_0
	echo "photometry_files:" > ../$1_yaml/$f.yaml
	echo "    $f" >> ../$1_yaml/$f.yaml
	echo "starting_parameters:" >> ../$1_yaml/$f.yaml
	echo "    t_0: gauss $t 0.1" >> ../$1_yaml/$f.yaml
	echo "    u_0: uniform 0.001 1." >> ../$1_yaml/$f.yaml
	echo "    t_E: gauss 20. 5." >> ../$1_yaml/$f.yaml
	echo "min_values:" >> ../$1_yaml/$f.yaml
	echo "    u_0: 0." >> ../$1_yaml/$f.yaml
	echo "    t_E: 0." >> ../$1_yaml/$f.yaml
	echo "fitting_parameters:" >> ../$1_yaml/$f.yaml
	echo "    n_steps: 5000" >> ../$1_yaml/$f.yaml
	echo "plots:" >> ../$1_yaml/$f.yaml
	echo "    best model:" >> ../$1_yaml/$f.yaml
	echo "        file: ../$1_png/$f.png" >> ../$1_yaml/$f.yaml
	#python3 ../ulens_model_fit.py moje.yaml
done
