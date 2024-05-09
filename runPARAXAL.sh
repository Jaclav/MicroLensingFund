#!/bin/bash

for i in {05,06,15,39,57,58,59}
do
  file=$1/PAR-$i-noaver.dat
  echo $file+.yaml
  echo $file-.yaml

  python3 ulens_model_fit.py $file+.yaml 1> $file+.OUT 2>$file+.ERR&
  python3 ulens_model_fit.py $file-.yaml 1> $file-.OUT 2>$file-.ERR&
  if((i % 2 ==0))
  then
    sleep 600
  fi
done
