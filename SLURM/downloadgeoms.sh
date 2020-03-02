#!/bin/bash

here=/storage/epp2/phumhf/MICE/runManagement
MICEvers=/warwick/epp/maus.git
GeomDir=/storage/epp2/phumhf/MICE/Geometries

#cd ~/MICE/maus/
#cd $MICEvers
. $MICEvers/env.sh
#file=$1

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

#bsub -G micegrp " 
echo -en "#!/bin/bash \n\
#SBATCH --ntasks=1
#SBATCH --mem-per-cpu=2012

cd $MICEvers \n\
. env.sh \n\
python $MICEvers/bin/utilities/download_geometry.py --geometry_download_by run_number --geometry_download_run_number ${runnumber} --geometry_download_directory $GeomDir/runnumber_${runnumber}   \n\
" \
| tee $here/logs/tmp/geoms${rn}.sh
chmod +x $here/logs/tmp/geoms${rn}.sh
sbatch -o $here/logs/geoms${rn}.log $here/logs/tmp/geoms${rn}.sh
#sbatch -p epp -o $here/logs/geoms${rn}.log $here/logs/tmp/geoms${rn}.sh


  fi
else 
echo "already have runnumber_${runnumber} geom"
fi

done < $file
done
