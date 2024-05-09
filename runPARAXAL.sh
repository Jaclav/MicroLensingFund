#!/bin/bash

for i in {5,6,15,39,57,58,59}
do
  file=$1/PAR-$i-noaver.dat
  echo $file.p.yaml
  echo $file.m.yaml

  python3 ulens_model_fit.py $file.p.yaml 1> $file.p.OUT 2>$file.p.ERR&
  python3 ulens_model_fit.py $file.m.yaml 1> $file.m.OUT 2>$file.m.ERR&
  sleep 600
done
