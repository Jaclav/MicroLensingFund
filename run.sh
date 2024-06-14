#!/bin/bash



  file=$1/PAR-06-noaver.dat-


  python3 ulens_model_fit.py $file.yaml 1> $file.OUT 2>$file.ERR&
