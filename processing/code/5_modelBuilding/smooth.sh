#!/bin/bash

# file="vrms_cmps_completos.bin"
# exit="vrms_cmps_completos_smooth.bin"

nx=1810
nz=501

file="vint_final.bin"
exit="vint_final_smooth.bin"

nx=2772
nz=340

times=10

gcc vagarosidade.c -o vag.exe
./vag.exe $file $nx $nz slowness.bin

smooth2 n1=$nz n2=$nx r1=5 r2=5 <slowness.bin >slsmooth.bin

for ii in $(seq 1 $times); do
    smooth2 n1=$nz n2=$nx r1=10 r2=10 <slsmooth.bin >aux.bin
    smooth2 n1=$nz n2=$nx r1=10 r2=10 <aux.bin >slsmooth.bin
done

./vag.exe slsmooth.bin $nx $nz $exit

rm vag.exe aux.bin slsmooth.bin slowness.bin
