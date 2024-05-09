#!/bin/bash

#./run 0 9 SIM
#PAR-01.1 -- PAR-01.10
#./run 10 19 SIM
#PAR-02.1 -- PAR-02.10

for ((i=$1;i<=$2;i++))
do

  

  file=$3/PAR-$i-noaver.dat
  echo $file.p.yaml
  echo $file.m.yaml

  python3 ulens_model_fit.py $file.p.yaml 1> $file.p.OUT 2>$file.p.ERR&
  python3 ulens_model_fit.py $file.m.yaml 1> $file.m.OUT 2>$file.m.ERR&
  if(($i%10==9))
  then
  sleep 1500
  fi	
done
