#!/bin/bash

for ((i=$1;i<=$2;i++))
do
	dataNum=$i
    if ((dataNum<10))
    then
    dataNum="0${dataNum}"
    fi
	echo $3/PAR-$dataNum-noaver.dat.yaml
    python3 ulens_model_fit.py $3/PAR-$dataNum-noaver.dat.yaml 1> $3/PAR-$dataNum-noaver.dat.OUT 2>$3/PAR-$dataNum-noaver.dat.ERR&
done