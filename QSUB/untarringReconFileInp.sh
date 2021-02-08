#!/bin/bash

headdir=/vols/mice/tlord1
here=/vols/mice/tlord1/runManagement
TARdir=/vols/mice/tlord1/tarballs
DATAversion=reconstructedOffline-v3.3.2
MAUSvers=Mausv3.3.2


#tardir=reconstructedOffline
#tardir=reconstructedOffline-v3.3.2

#datadir=merge-07-19

#for i in 7469 `seq 9395 9399` `seq 10579 10603`; do 
#for i in 9885 9903 ; do
#for i in 10327 ; do

for file in "$@"; do
while read -r line ; do
  #echo $line
  i=$(echo "${line}" |  cut -d'|' -f1 )
  echo $i

  if [ $i -lt 10000 ] 
  then
    rn=0$i
  else
    rn=$i
  fi  

  if [ ! -f $headdir/ReconData/$MAUSvers/${rn}/${rn}_recon.root ] ; then

  mkdir -p $headdir/ReconData/$MAUSvers/${rn}

echo -en "#!/bin/bash \n\

cd $headdir/ReconData/$MAUSvers/${rn} ;  tar -xvf $headdir/tarballs/$DATAversion/${rn}_offline.tar
" \
| tee $here/logs/tmp/untar_${rn}.sh

chmod +x $here/logs/tmp/untar_${rn}.sh

qsub -q hep.q -l h_rt=01:00:00 -wd $here/logs/ $here/logs/tmp/untar_${rn}.sh

else
echo "Already untarred this file"
fi  

done < $file
done

