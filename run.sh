#!/bin/bash
count=0
cpu_count=$(nproc)
for file in "$1"/*
do
    if [[ $file == *.yaml ]]; then
        file2=${file%.*}
        echo $file2
        python3 ulens_model_fit.py $file2.yaml 1> $file2.OUT 2>$file2.ERR&
        count=$((count+1))
        if [ $count -eq $cpu_count ]; then
            wait
            count=0
        fi
    fi
done
