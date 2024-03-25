#! /bin/tcsh

foreach f ( $1/*.yaml )
  ( python3 ulens_model_fit.py $f > $f:r.OUT ) >& $f:r.ERR &
end

