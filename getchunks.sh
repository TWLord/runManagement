CHUNK_PATH="/data/mice/phumhf/G4BLChunks/Mausv3.3.2"

for run in 9763; do 
  mkdir ${CHUNK_PATH}/$run/ 
  for i in `seq 100 399` ; do
    wget http://gfe02.grid.hep.ph.ic.ac.uk:8301/dmaletic/G4BL_Tom/10_200M3_Test1v3/G4BLoutput_10_200M3_Test1v3_${i}.json ${CHUNK_PATH}/$run/
  done
done
