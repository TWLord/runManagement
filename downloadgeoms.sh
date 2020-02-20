#!/bin/bash

MICEvers=~/MICE/maus--versions/MAUSv3.3.2/

#cd ~/MICE/maus/
cd $MICEvers
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

if [ ! -e /data/mice/phumhf/Geometries/runnumber_${runnumber}/ ] ; then

  mkdir -p /data/mice/phumhf/Geometries/runnumber_${runnumber}/

  if [ ! -e /data/mice/phumhf/Geometries/runnumber_${runnumber}/ParentGeometryFile.dat ] ; then

bsub -G micegrp " 
#cd ~/MICE/maus/ 
cd $MICEvers
. env.sh 
python $MICEvers/bin/utilities/download_geometry.py --geometry_download_by run_number --geometry_download_run_number ${runnumber} --geometry_download_directory /data/mice/phumhf/Geometries/runnumber_${runnumber}"
#^D


  fi
else 
echo "already have runnumber_${runnumber} geom"
fi

done < $file
done
