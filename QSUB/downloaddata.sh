#!/bin/bash

here=/vols/mice/tlord1/runManagement
MAUSdir=/vols/mice/tlord1/maus--versions/MAUSv3.3.2
TARdir=/vols/mice/tlord1/tarballs
DATAversion=reconstructedOffline-v3.3.2

cd $MAUSdir
. env.sh
#file=$1

mkdir -p $TARdir/$DATAversion
mkdir -p $TARdir/WGETlog

for file in "$@" ; do
while read -r line ; do
#echo $line
 rn=$(echo "${line}" |  cut -d'|' -f1 )
 echo $rn


if [ $rn -lt 10000 ] ; then
runnumber=0$rn
else 
runnumber=$rn
fi

if [ ! -e $TARdir/$DATAversion/${runnumber}_offline.tar ] ; then

echo -en "#!/bin/bash \n\

wget -P $TARdir/$DATAversion/ http://reco.mice.rl.ac.uk/MAUS-v3.3.2/${runnumber}_offline.tar 
" \
| tee $here/logs/tmp/tar_${runnumber}.sh

chmod +x $here/logs/tmp/tar_${runnumber}.sh
qsub -q hep.q -l h_rt=01:00:00 -wd $TARdir/WGETlog/ $here/logs/tmp/tar_${runnumber}.sh


else 
echo "already have run_${runnumber} data"
fi

done < $file
done
