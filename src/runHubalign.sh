#!/bin/bash

#############################################################
# extract labels by using hubalign
#############################################################

cp HubAlign ./../data/rawData/
cp runHubalign.py ./../data/rawData/
mkdir -p ./../data/hubLabel/
cp hubalignEC.py ./../data/hubLabel/
cp hubalignLCCS.py ./../data/hubLabel/
cd ./../data/rawData/
# run hubalign to get raw label files, $1: dbStart, $2: dbEnd, $3: queryStart, $4: queryEnd
python runHubalign.py $1 $2 $3 $4 >> outputHub  
rm HubAlign
rm runHubalign.py
rm outputHub
rm *.alignment
mv *.eval ./../hubLabel/
cd ./../hubLabel/
python hubalignEC.py $1 $2  # get label hubalign ec
python hubalignLCCS.py $1 $2  # get label hubalign lccs
rm hubalignEC.py
rm hubalignLCCS.py
rm *.eval