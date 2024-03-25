#!/bin/bash
#run: ./yamlgen.sh P1
mkdir $1 || (echo "Dir $1 already exists";exit -1)	#create dir named P1
mkdir $1/yaml
mkdir $1/png
cd dataPoleski
ls | while read f;						#read files from dataPoleski
do
	read t0 u0 tE A < <(python3 ../scripts/super_mega_script.py $f 2>/dev/null)
	#t0=`python3 ../scripts/t0.py $f` 	#t_0
	#u0=`python3 ../scripts/u0.py $f` 	#u_0
	file=../$1/yaml/$f.yaml				#result .yaml file
	#YAML file
	echo "photometry_files:" > $file
	echo "    dataPoleski/$f" >> $file
	echo "starting_parameters:" >> $file
	echo "    t_0: gauss 245$t0 0.1" >> $file	#short Julian to long Julian
	echo "    u_0: uniform $u0 1." >> $file		#TODO: add uncertanity
	echo "    t_E: gauss $tE 5." >> $file
	echo "min_values:" >> $file
	echo "    u_0: 0." >> $file
	echo "    t_E: 0." >> $file
	echo "fitting_parameters:" >> $file
	echo "    n_steps: 5000" >> $file
	echo "plots:" >> $file
	echo "    best model:" >> $file
	echo "        file: $1/png/$f.png" >> $file
done
