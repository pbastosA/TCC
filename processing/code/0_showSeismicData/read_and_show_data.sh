#!/bin/bash

segy_path1="../../rawData/MGFLT/OGA.2016.SWB.WG162D.001.MGFLT.CMP.L14.SGY"
CDP_path1="../../rawData/MGFLT/seismic_data_CDP.su"

segy_path2="../../rawData/MGRAW/OGA.2016.SWB.WG162D.001.MGRAW.CMP.L14.SGY"
CDP_path2="../../rawData/MGRAW/seismic_data_CDP.su"

segy_path3="../../rawData/PREMIG/OGA.2016.SWB.WG162D.001.PREMIG.CMP.L14.SGY"
CDP_path3="../../rawData/PREMIG/seismic_data_CDP.su"

# echo "Lendo o dado "$segy_path1
# segyread tape=$segy_path1 verbose=1 | segyclean >$CDP_aux1

# echo "Lendo o dado "$segy_path2
# segyread tape=$segy_path2 verbose=1 | segyclean >$CDP_aux2

# echo "Lendo o dado "$segy_path3
# segyread tape=$segy_path3 verbose=1 | segyclean >$CDP_aux3

# Removendo os arquivos binários
# rm binary header

# Para visualizar os cdps completos (conferir se estão iguais)
# sukeycount <$CDP_path1 key=cdp | more 
# sukeycount <$CDP_path2 key=cdp | more
# sukeycount <$CDP_path2 key=cdp | more 

# Visualizando dados no domínio CDP
# suwind <$CDP_path1 key=cdp min=$cdp max=$cdp | suximage perc=99 &
# suwind <$CDP_path2 key=cdp min=$cdp max=$cdp | suximage perc=99 &
# suwind <$CDP_path3 key=cdp min=$cdp max=$cdp | suximage perc=99 &

# Separando cdps para a análise {in range(9943,13561,2)} [somente ímpares nesse intervalo]
cdp=10123

suwind <$CDP_path1 key=cdp min=$cdp max=$cdp > cdp_flt_$cdp.su
suwind <$CDP_path2 key=cdp min=$cdp max=$cdp > cdp_raw_$cdp.su
suwind <$CDP_path3 key=cdp min=$cdp max=$cdp > cdp_mig_$cdp.su

# Observando o espectro de amplitude

# suspecfx <cdp_flt_$cdp.su | suximage perc=99 legend=1 title="Flat" &
# suspecfx <cdp_raw_$cdp.su | suximage perc=99 legend=1 title="Raw" &
# suspecfx <cdp_mig_$cdp.su | suximage perc=99 legend=1 title="Mig" &

# suwind <cdp_9943.su key=tracl min=25460 max=25600 >cdp_mod_9943.su
# suspecfx <cdp_mod_9943.su | suximage perc=99 legend=1 &
# suvelan nv=150 fv=5500 dv=15 <cdp_mod_9943.su | suximage d2=15 f2=5500 verbose=1 cmap=hsv2 legend=1 bclip=.5 &

# Observando o espectro de fase (fase zero!)
# sufft <cdp_flt_$cdp.su | suamp mode=amp | suximage title="Flat" label1="Frequency [Hz]" label2="Traces" legend=1 perc=99 &
# sufft <cdp_raw_$cdp.su | suamp mode=amp | suximage title="Raw" label1="Frequency [Hz]" label2="Traces" legend=1 perc=99 &
# sufft <cdp_mig_$cdp.su | suamp mode=amp | suximage title="Mig" label1="Frequency [Hz]" label2="Traces" legend=1 perc=99 &

# Retirando um traço do dado 


echo "Tudo certo!"
