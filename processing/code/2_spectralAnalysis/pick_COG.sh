#!/bin/bash

file="../../rawData/MGRAW/seismic_data_OFFSET.su"

# suwind <$file key=offset min=100 max=100 | sustrip >nearOffset.bin &
suwind <$file key=offset min=100 max=100 | suximage perc=99 &
