#!/bin/bash

i=$1
for f in sim_26_16_16/yaml2/*.yaml
do
  if ((i<=$2))
  then
    echo $f
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

    echo sim_26_16_16/yaml2/PAR-$dataNum-noaver.dat.$xi_P.yaml
    echo $i
    i=$((i+1))
  fi
done