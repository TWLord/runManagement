#!/bin/bash

set -- 1 2 3 4 5 6
while [ "$#" -gt 0 ]; do

  rn=$1
  MCn=$2
  echo "$1:$2"
  echo "$rn  & $MCn"
  shift 2
  echo "$1:$2"
  echo "$rn  & $MCn"

done
