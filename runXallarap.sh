#!/bin/bash

#./run 0 9 SIM
#PAR-01.1 -- PAR-01.10
#./run 10 19 SIM
#PAR-02.1 -- PAR-02.10

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

  file=$3/PAR-$dataNum-noaver.dat.$xi_P
  echo $file.yaml
  python3 ulens_model_fit.py $file.yaml 1> $file.OUT 2>$file.ERR&
  if(($i%30==29))
  then
  sleep 600
  fi	
done
