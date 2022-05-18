#!/bin/bash

CDP_path="../../rawData/PREMIG/seismic_data_CDP.su"
SHOT_path="../../rawData/PREMIG/seismic_data_SHOT.su"

# Organizando o arquivo no domínio do tiro
# susort <$CDP_path fldr offset >$SHOT_path

# Extraindo as posições da geometria 
# sugethw <$SHOT_path fldr >>"../../parameters/FFID.txt"
# sugethw <$SHOT_path sx sy >>"../../parameters/source_UTM_coordinates.txt"
# sugethw <$SHOT_path gx gy >>"../../parameters/receiver_UTM_coordinates.txt"

python3 plot_seismic.py