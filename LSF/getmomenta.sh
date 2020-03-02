#!/bin/bash

#CC=2017-02-6 
for CC in "2017-02-6" "2017-02-5" "2017-02-2" "2017-02-1" "2016-05-1-SSUSSD" "2016-04-2.4a" "2016-04-1.5" "2016-04-1.7" "2016-04-1.2" "2016-05-1" "M2D-flip-2017-02-5" ; do
dest=~/MICE/runManagement/MomFiles/$CC/
mkdir $dest

for i in `seq 140 350`; do
 for ABS in "ABS-LH2" "ABS-LH2-EMPTY" "ABS-SOLID-EMPTY" "ABS-SOLID-LiH" ; do 

  python sortStep4runs.py --CC $CC --momentum $i --magnet solenoid --absorber $ABS --dest $dest step4-runs.txt 

 done
done
done
