#!/bin/bash
here=/storage/epp2/phumhf/MICE/runManagement
MAUSdir=/storage/epp2/phumhf/MICE/maus--versions/MAUSv3.3.2
TARdir=/storage/epp2/mice/phumhf/tarballs
DATAversion=reconstructedOffline-v3.3.2
#DATAdir=/storage/epp2/mice/phumhf/ReconData/$DATAversion
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

sbatch --mem 2012 -o $TARdir/WGETlog/${runnumber}.log --wrap " 
wget -P $TARdir/$DATAversion/ http://reco.mice.rl.ac.uk/MAUS-v3.3.2/${runnumber}_offline.tar ; 
"


#sbatch -o $TARdir/WGETlog/${runnumber}.log  <<EOF 
##!/bin/bash
#wget -P $TARdir/$DATAversion/ http://reco.mice.rl.ac.uk/MAUS-v3.3.2/${runnumber}_offline.tar
#EOF

else 
echo "already have run_${runnumber} data"
fi

done < $file
done
