#!/bin/bash

i=$1
for f in sim_26_16_16/yaml/*.yaml
do
  if ((i<$2))
  then
    i=$((i+1))
	dataNum=$i
    if ((dataNum<10))
    then
    dataNum="0${dataNum}"
    fi
	echo $3/PAR-$dataNum-noaver.dat.yaml
    python3 ulens_model_fit.py $3/PAR-$dataNum-noaver.dat.yaml 1> $3/PAR-$dataNum-noaver.dat.OUT 2>$3/PAR-$dataNum-noaver.dat.ERR&
  fi
done