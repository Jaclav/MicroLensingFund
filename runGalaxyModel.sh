#!/bin/bash


for file in "$1"/*
do
    if [[ $file == *.yaml ]]; then
        echo $file
        python3 microlensing_black_holes/single_parallax_fit_geocentric.py $file&
    fi
done