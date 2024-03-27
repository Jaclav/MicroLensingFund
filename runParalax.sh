#!/bin/bash

for ((i=$1;i<=$2;i++))
do
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
  python3 ulens_model_fit.py $3/PAR-$dataNum-noaver.dat.$xi_P.yaml 1> $3/PAR-$dataNum-noaver.dat.$xi_P.OUT 2>$3/PAR-$dataNum-noaver.dat.$xi_P.ERR&
done