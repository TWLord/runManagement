#!/bin/bash

CC="2017_03"
downloaddir="/data/mice/phumhf/HallProbes/$CC"
mkdir -p $downloaddir

file=$1
#for file in "$1" ; do
while read -r line ; do
echo $line

wget -P $downloaddir "http://heplnv152.pp.rl.ac.uk/analysis/process_variables/v0/$CC/Hall_probes/$line" 

done < $file 
#done
