#!/bin/bash

cd ~/MICE/maus/
. env.sh
#file=$1
loc="http://gfe02.grid.hep.ph.ic.ac.uk:8301/MICE/Step4"

for file in "$@" ; do
while read -r line ; do
#echo $line
 rn=$(echo "${line}" |  cut -d'|' -f1 )
 echo $rn

let rN=(${rn}/100)*100
roundN=$( printf "%05d" $rN )
echo "Raw Data serial : $rn "
echo "Raw Data round : $roundN "

if [ $rn -lt 10000 ] ; then
runnumber=0$rn
else 
runnumber=$rn
fi

if [ ! -e /data/mice/phumhf/tarballs/raw/${runnumber}.tar ] ; then

  bsub -G micegrp -eo ~/WGETlog/raw_${runnumber}.log -q medium "wget -P /data/mice/phumhf/tarballs/raw/ $loc/$roundN/${runnumber}.tar"

  #wget -P /data/mice/phumhf/tarballs/reconstructedOffline-v3.3.2/ http://reco.mice.rl.ac.uk/MAUS-v3.3.2/${runnumber}_offline.tar

else 
echo "already have run_${runnumber} raw data"
fi

done < $file
done
