#!/bin/bash

i=$1
for f in sim_26_16_16/yaml2/*.yaml
do
  if ((i<=$2))
  then
    xi_P=$(($i%10))
    if (($xi_P==0))
    then
      xi_P=10
    fi

    dataNum=$(($i/10+1))
    if ((dataNum<10))
    then
    dataNum="0${dataNum}"
    fi

    echo $3/PAR-$dataNum-noaver.dat.$xi_P.yaml
    python3 ulens_model_fit.py $3/PAR-$dataNum-noaver.dat.yaml 1> $3/PAR-$dataNum-noaver.dat.OUT 2>$3/PAR-$dataNum-noaver.dat.ERR&
    i=$((i+1))
  fi
done