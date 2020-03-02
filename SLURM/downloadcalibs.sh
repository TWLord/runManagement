#!/bin/bash

#MAUSDIR=~/MICE/maus--versions/MAUSv3.3.0
here=/storage/epp2/phumhf/MICE/runManagement
MAUSDIR=/storage/epp2/phumhf/MICE/maus--versions/MAUSv3.3.2
CalibDir=/storage/epp2/phumhf/MICE/Calibration
#cd ~/MICE/maus/
#cd $MAUSDIR 
. $MAUSDIR/env.sh
#file=$1

for file in "$@" ; do
while read -r line ; do
#echo $line
 runnumber=$(echo "${line}" |  cut -d'|' -f1 )
 #echo $rn


if [ ! -e $CalibDir/files/cabling/${runnumber}/ ] ; then

mkdir -p $CalibDir/files/cabling/${runnumber}/

#bsub -G micegrp -q express " 
#echo "
#sbatch -o $here/logs/calib${rn}.sh " 
echo -en "#!/bin/bash \n\
#SBATCH --ntasks=1 \n\
#SBATCH --partition epp \n\
module purge 
 ####SBATCH --mem-per-cpu=2012 \n\


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
sbatch -o $here/logs/calib${runnumber}.log $here/logs/tmp/calib${runnumber}.sh
 

else 
echo "already have ${runnumber} calib"
fi

done < $file
done
