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

for rn in 9921 8881 9769 9921 8916 10148 ; do
 echo $rn

let MCr=(${rn}/100)*100
MCnround=$( printf "%05d" $MCr )
echo "MC round : $MCnround "

if [ $rn -lt 10000 ] ; then
runnumber=0$rn
else 
runnumber=$rn
fi

if [ ! -e $TARdir/$DATAversion/${runnumber}_offline.tar ] ; then

sbatch -p epp --mem 2012 -o $TARdir/WGETlog/${runnumber}.log --wrap " 
# wget -P $TARdir/$DATAversion/ http://reco.mice.rl.ac.uk/MAUS-v3.3.2/${runnumber}_offline.tar ; 
wget -P $TARdir/$DATAversion/ http://gfe02.grid.hep.ph.ic.ac.uk:8301/RECO/MAUS-v3.3.2/1/Step4/${MCnround}/${runnumber}_offline.tar ; 
"

#sbatch -o $TARdir/WGETlog/${runnumber}.log  <<EOF 
##!/bin/bash
#wget -P $TARdir/$DATAversion/ http://reco.mice.rl.ac.uk/MAUS-v3.3.2/${runnumber}_offline.tar
#EOF

else 
echo "already downloaded run_${runnumber} data tarball"
fi

done
