#!/bin/bash

flt_path="CMP10123/cdp_flt_10123.su"
raw_path="CMP10123/cdp_raw_10123.su"
mig_path="CMP10123/cdp_mig_10123.su"

# Tirando os espectros de amplitude

# suspecfx <$flt_path | sustrip > "CMP10123/espectro_amplitude_flt.bin" 
# suspecfx <$raw_path | sustrip > "CMP10123/espectro_amplitude_raw.bin" 
# suspecfx <$mig_path | sustrip > "CMP10123/espectro_amplitude_mig.bin" 

# Tirando os espectros de fase

# sufft <$flt_path | suamp mode=phase | sustrip > "CMP10123/espectro_fase_flt.bin"
# sufft <$raw_path | suamp mode=phase | sustrip > "CMP10123/espectro_fase_raw.bin" 
# sufft <$mig_path | suamp mode=phase | sustrip > "CMP10123/espectro_fase_mig.bin" 

# Tirando o semblance dos CMPs 9945, 11263, 13543
CDP_path2="../../rawData/MGRAW/seismic_data_CDP.su"

suwind <$CDP_path2 key=cdp min=9945 max=9945 | suvelan nv=150 fv=1500 dv=30 | sustrip >"CMP10123/semblance_CMP_raw_9945.bin" 
suwind <$CDP_path2 key=cdp min=11263 max=11263 | suvelan nv=150 fv=1500 dv=30 | sustrip >"CMP10123/semblance_CMP_raw_11263.bin" 
suwind <$CDP_path2 key=cdp min=13543 max=13543 | suvelan nv=150 fv=1500 dv=30 | sustrip >"CMP10123/semblance_CMP_raw_13543.bin" 
