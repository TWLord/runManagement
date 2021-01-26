#!/bin/bash

here=/vols/mice/tlord1/runManagement
MAUSDIR=/vols/mice/tlord1/maus--versions/MAUSv3.3.2
CalibDir=/vols/mice/tlord1/Calibration

. $MAUSDIR/env.sh

for file in "$@" ; do
while read -r line ; do
#echo $line
 runnumber=$(echo "${line}" |  cut -d'|' -f1 )
 #echo $rn


if [ ! -e $CalibDir/files/cabling/${runnumber}/ ] ; then

mkdir -p $CalibDir/files/cabling/${runnumber}/

echo -en "#!/bin/bash \n\


cd $MAUSDIR \n\
. env.sh \n\

#python $MAUSDIR/src/common_py/calibration/get_scifi_calib.py --SciFiCalibMethod Run --SciFiCalibSrc ${runnumber} --SciFiConfigDir $CalibDir/${runnumber} \n\

python $MAUSDIR/src/common_py/calibration/get_scifi_calib.py --SciFiCalibMethod Run --SciFiCalibSrc ${runnumber} --SciFiConfigDir $CalibDir  \n\

#mv $CalibDir/files/cabling/${runnumber}/* $CalibDir/${runnumber}/ \n\
#mv $CalibDir/files/calibration/${runnumber}/* $CalibDir/${runnumber}/ \n\

#rm -rf $CalibDir/files/cabling/${runnumber}/ \n\
#rm -rf $CalibDir/files/calibration/${runnumber}/ \n\
" \
| tee $here/logs/tmp/calib${runnumber}.sh
chmod +x $here/logs/tmp/calib${runnumber}.sh
qsub -q hep.q -l h_rt=00:20:00 -wd $here/logs/ $here/logs/tmp/calib${runnumber}.sh
 

else 
echo "already have ${runnumber} calib"
fi

done < $file
done
