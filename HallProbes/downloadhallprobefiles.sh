#!/bin/bash

#CC="2017_01"
for CC in "2017_01" "2016_05" "2016_04" "2016_03" "2016_02" "2016_01" "2015_04" "2015_03" "2015_02" "2015_01b" "2015_01a"; do

downloaddir="/data/mice/phumhf/HallProbes/$CC"
mkdir -p $downloaddir

file=$1
#for file in "$1" ; do
while read -r line ; do
echo $line

wget -P $downloaddir "http://heplnv152.pp.rl.ac.uk/analysis/process_variables/v0/$CC/Hall_probes/$line" 

done < $file 

done
