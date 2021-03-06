#!/bin/bash

cd ~/MICE/maus/
. env.sh
#file=$1

#for file in "$@" ; do
#while read -r line ; do
#echo $line
# rn=$(echo "${line}" |  cut -d'|' -f1 )
# echo $rn

MCversion=MCv3.3.2
#rn=9886
##rn=9886
##MCn=229
set -- 10268 259 9911 260 9910 261 10267 262 9909 263 10265 264  
#set -- 10243 242 10245 243 10246 244 10314 245 10317 246 10318 247 10319 248 9883 253 9885 254 9886 255 10508 256 10504 257 10509 258 
#set -- 10243 242 10245 243 10246 244 10314 245 10317 246 10318 247 10319 248 9883 253 9885 254 9886 255
#set -- 10508 256 10504 257 10509 258 
while [ "$#" -gt 0 ]; do

rn=$1
MCn=$2
shift 2

let MCr=(${MCn}/100)*100
fnstart=0
fnend=19

if [ $rn -lt 10000 ] ; then
runnumber=0$rn
else 
runnumber=$rn
fi

echo "run: $runnumber "

MCnumber=$( printf "%06d" $MCn )
echo "MC serial : $MCnumber "
MCnround=$( printf "%06d" $MCr )
echo "MC round : $MCnround "

mkdir -p /data/mice/phumhf/tarballs/$MCversion/$runnumber/

for it in `seq ${fnstart} ${fnend}`; do
iter=$( printf "%05d" $it )
echo $iter


if [ ! -e /data/mice/phumhf/tarballs/$MCversion/$runnumber/${iter}_mc.tar ] ; then

#  bsub -G micegrp -oo ~/WGETlog/MC_${runnumber}_${iter}.log -q express "wget -P /data/mice/phumhf/tarballs/$MCversion/$runnumber/ http://gfe02.grid.hep.ph.ic.ac.uk:8301/Simulation/MCproduction/000000/${MCnround}/${MCnumber}/${iter}_mc.tar"

  bsub -G micegrp -oo ~/WGETlog/MC_${runnumber}_${iter}.log -q express "wget -P /data/mice/phumhf/tarballs/$MCversion/$runnumber/ http://gfe02.grid.hep.ph.ic.ac.uk:8301/dmaletic/MCproduction/000000/${MCnround}/${MCnumber}/${iter}_mc.tar"

  #wget -P /data/mice/phumhf/tarballs/$MCversion/$runnumber/ http://gfe02.grid.hep.ph.ic.ac.uk:8301/Simulation/MCproduction/000000/${MCnround}/${MCnumber}/${iter}_mc.tar

else 
echo "already have run_${runnumber} ${iter}_mc.tar"
fi


#done < $file
done

#echo "\nfiles downloaded for run:${runnumber}\n  MC serialnumber :${MCn}\n Downloaded files:${fnstart} to ${fnend}\n  " | tee -a /data/mice/phumhf/tarballs/$MCversion/$runnumber/downloadinfo.txt
printf "\nfiles downloaded for run:${runnumber}\nMC serialnumber:${MCn}\nDownloaded files:${fnstart} to ${fnend}\n " | tee -a /data/mice/phumhf/tarballs/$MCversion/$runnumber/downloadinfo.txt


done
