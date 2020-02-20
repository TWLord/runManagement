#!/bin/bash

MAUSDIR=~/MICE/maus--versions/MAUSv3.3.0
#cd ~/MICE/maus/
cd $MAUSDIR 
. env.sh
#file=$1

for file in "$@" ; do
while read -r line ; do
#echo $line
 runnumber=$(echo "${line}" |  cut -d'|' -f1 )
 echo $rn


if [ ! -e /data/mice/phumhf/Calibration/${runnumber}/ ] ; then

mkdir -p /data/mice/phumhf/Calibration/${runnumber}/

bsub -G micegrp -q express " 
cd $MAUSDIR
. env.sh 

#python $MAUSDIR/src/common_py/calibration/get_scifi_calib.py --SciFiCalibMethod Run --SciFiCalibSrc ${runnumber} --SciFiConfigDir /data/mice/phumhf/Calibration/${runnumber} 

python $MAUSDIR/src/common_py/calibration/get_scifi_calib.py --SciFiCalibMethod Run --SciFiCalibSrc ${runnumber} --SciFiConfigDir /data/mice/phumhf/Calibration 

#mv /data/mice/phumhf/Calibration/files/cabling/${runnumber}/* /data/mice/phumhf/Calibration/${runnumber}/
#mv /data/mice/phumhf/Calibration/files/calibration/${runnumber}/* /data/mice/phumhf/Calibration/${runnumber}/

#rm -rf /data/mice/phumhf/Calibration/files/cabling/${runnumber}/
#rm -rf /data/mice/phumhf/Calibration/files/calibration/${runnumber}/
"

else 
echo "already have ${runnumber} calib"
fi

done < $file
done
