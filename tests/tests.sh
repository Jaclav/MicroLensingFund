echo "u0.py"
echo 0.13 vs `python3 ../scripts/u0.py OB03235_OGLE.txt`
echo "55.5 vs" `python3 ../scripts/u0.py phot_ob08092_O4.dat`
echo "0.375 vs " `python3 ../scripts/u0.py starBLG234.6.I.218982.dat`
echo "t0.py"
echo "2848.0 vs " `python3 ../scripts/t0.py OB03235_OGLE.txt`
echo "5379.4 vs " `python3 ../scripts/t0.py phot_ob08092_O4.dat`
echo "3628.3 vs " `python3 ../scripts/t0.py starBLG234.6.I.218982.dat`
echo "tE.py"
echo "61.5 vs " `python3 ../scripts/tE.py OB03235_OGLE.txt`
echo "16 vs " `python3 ../scripts/tE.py phot_ob08092_O4.dat`
echo "102 vs " `python3 ../scripts/tE.py starBLG234.6.I.218982.dat`