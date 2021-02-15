#!/bin/bash

here=/vols/mice/tlord1/runManagement
MICEvers=/vols/mice/tlord1/maus--versions/MAUSv3.3.2
GeomDir=/vols/mice/tlord1/Geometries

. $MICEvers/env.sh

mkdir -p $here/logs/tmp

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

if [ ! -e $GeomDir/runnumber_${runnumber}/ ] ; then

  mkdir -p $GeomDir/runnumber_${runnumber}/

  if [ ! -e $GeomDir/runnumber_${runnumber}/ParentGeometryFile.dat ] ; then

echo -en "#!/bin/bash \n\

cd $MICEvers \n\
. env.sh \n\
python $MICEvers/bin/utilities/download_geometry.py --geometry_download_by run_number --geometry_download_run_number ${runnumber} --geometry_download_directory $GeomDir/runnumber_${runnumber}   \n\
" \
| tee $here/logs/tmp/geoms${rn}.sh
chmod +x $here/logs/tmp/geoms${rn}.sh
qsub -q hep.q -l h_rt=00:20:00 -wd $here/logs/ $here/logs/tmp/geoms${rn}.sh


  fi
else 
echo "already have runnumber_${runnumber} geom"
fi

done < $file
done
