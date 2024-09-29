#!/bin/bash

count=0
cpu_count=$(nproc)

for file in "$1"/*
do
    if [[ $file == *.yaml ]]; then
        file2=${file%.*}
        echo $file2

        python3 microlensing_black_holes/single_parallax_fit_geocentric.py $file&
        count=$((count+1))
        if [ $count -eq $cpu_count ]; then
            wait
            count=0
        fi
    fi
done