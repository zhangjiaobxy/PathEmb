#!/bin/bash

#############################################################
# extract labels by using netal
#############################################################

cp NETAL ./../data/rawData/
cp runNetal.py ./../data/rawData/
mkdir -p ./../data/netalLabel/
cp netalEC.py ./../data/netalLabel/
cp netalLCCS.py ./../data/netalLabel/
cd ./../data/rawData/
# run netal to get raw label files, $1: dbStart, $2: dbEnd, $3: queryStart, $4: queryEnd
python runNetal.py $1 $2 $3 $4 >> outputNetal  
rm NETAL
rm runNetal.py
rm outputNetal
rm *.alignment
rm alignmentDetails.txt
rm simLog.txt
mv *.eval ./../netalLabel/
cd ./../netalLabel/
python netalEC.py $1 $2 # get label netal ec
python netalLCCS.py $1 $2 # get label netal lccs
rm netalEC.py
rm netalLCCS.py
rm *.eval