##################################################################
# Arquivos imutáveis
##################################################################

CDP_data="../../rawData/MGRAW/seismicDataCDP_processing.su"
cdp_min=9943
cdp_max=13561
dcdp=12.5

##################################################################
# Arquivo com as velocidades RMS para a correção NMO
##################################################################

#velocities="../4_velocityAnalysis/obs_vpick.txt"

velocities="vpick_corrigido.txt"

##################################################################
# Nomes dos arquivos de saída  
##################################################################

#STOLT_data="seismic_obsData_STOLT.su"

STOLT_data="seismic_calData_STOLT.su"

##################################################################
# Usando a analise de velocidades para empilhar o dado 
##################################################################

sunmo <$CDP_data par=$velocities | sustack | sustolt \
par=$velocities cdpmin=$cdp_min cdpmax=$cdp_max dxcdp=$dcdp \
>$STOLT_data
