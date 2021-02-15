#!/bin/bash

headdir=/vols/mice/tlord1
shdir=/vols/mice/tlord1/runManagement/logs/tmp

tardir=MCv3.3.2

MCversion=MAUSv3.3.2
prodversion=v3

#rn=9886
#MCn=202

#for opt in "10243,215" "10245,216" "10246,217" "10314,218" "10317,220" "10318,221" "10319,222" "10579,223" "10580,224" "10581,225" "10582,226" "9883,227" "9885,228" "9886,229" ; do
#for opt in "10243,242" "10245,243" "10246,244" "10314,245" "10317,246" "10318,247" "10319,248" "9883,253" "9885,254" "9886,255" ; do
#for opt in "10268,259" "9911,260" "9910,261" "10267,262" "9909,263" "10265,264" ; do
for opt in "9760,279" "9763,280" ; do
#for opt in "10508,256" "10504,257" "10509,258" ; do

rn="${opt%,*}"
MCn="${opt##*,}"
echo "rn = $rn"
echo "MCn = $MCn"
fnstart=100
fnend=399

if [ $rn -lt 10000 ] ; then
rn=0$rn
else 
rn=$rn
fi

runnumber=$rn$prodversion

echo "run: $runnumber "

MCnumber=$( printf "%06d" $MCn )
echo "MC serial : $MCnumber "


mkdir -p $headdir/MC/$MCversion/${runnumber}
mkdir -p $headdir/tarballs/$tardir/${rn}/logs

for it in `seq ${fnstart} ${fnend}`; do
iter=$( printf "%05d" $it )
echo $iter

if [ ! -e $headdir/MC/$MCversion/${runnumber}/${iter}_sim.root ] ; then

mkdir -p $headdir/MC/$MCversion/${runnumber}/${iter}

echo -en "#!/bin/bash \n\
cd $headdir/MC/$MCversion/${runnumber}/${iter} ;  tar -xvf $headdir/tarballs/$tardir/${rn}/${iter}_mc.tar ; mv ${iter}_sim.root ../ " \
| tee $shdir/untar_${iter}_mc.sh 

  chmod +x $shdir/untar_${iter}_mc.sh 
  qsub -q hep.q -l h_rt=01:00:00 -wd $headdir/tarballs/$tardir/${rn}/logs/ $shdir/untar_${iter}_mc.sh 
else
echo "already untarred run_$runnumber ${iter}_mc.tar"
fi

done

printf "\nfiles untarred for run:${runnumber}\nMC serialnumber:${MCn}\nDownloaded files:${fnstart} to ${fnend}\n " | tee -a $headdir/MC/$MCversion/$runnumber/untarinfo.txt

done
