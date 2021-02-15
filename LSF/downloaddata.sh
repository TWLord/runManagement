#!/bin/bash

cd ~/MICE/maus/
. env.sh
#file=$1

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

if [ ! -e /data/mice/phumhf/tarballs/reconstructedOffline-v3.3.2/${runnumber}_offline.tar ] ; then

  bsub -G micegrp -eo ~/WGETlog/${runnumber}.log -q medium "wget -P /data/mice/phumhf/tarballs/reconstructedOffline-v3.3.2/ http://reco.mice.rl.ac.uk/MAUS-v3.3.2/${runnumber}_offline.tar"

  #wget -P /data/mice/phumhf/tarballs/reconstructedOffline-v3.3.2/ http://reco.mice.rl.ac.uk/MAUS-v3.3.2/${runnumber}_offline.tar

else 
echo "already have run_${runnumber} data"
fi

done < $file
done
