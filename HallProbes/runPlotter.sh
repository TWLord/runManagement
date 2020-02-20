#!/bin/bash

# Want to get start & end date/time of runs from elsewhere then pass to plotter
# should be in runfile.txt 
for file in "$@"; do
while read -r line ; do
echo $line
 rn=$(echo "${line}" |  cut -d'|' -f1 )
 echo $rn

 starttime=$(echo "${line}" |  cut -d'|' -f2 )
 echo $starttime

#CC="2017_02"
#python plotHallProbes.py --dest /home/phumhf/MICE/runManagement/HallProbes/Plots/ --daystart 09/21/2017 --dayend 09/21/2017 --timestart 00:15:49.584023049 --timeend 21:44:00.00 /data/mice/phumhf/HallProbes/$CC/MICE-SS* 

done < $file
done
