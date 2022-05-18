##################################################################
# Arquivos imutáveis
##################################################################

CDP_data="../sintheticDataEngland_CDP.su"
cdp_min=80250
cdp_max=306250
dcdp=12.5

##################################################################
# Arquivo com as velocidades RMS para a correção NMO
##################################################################

velocities="vpick.txt"

##################################################################
# Nomes dos arquivos de saída 
##################################################################

STOLT_data="sintheticDataEngland_STOLT.su"

##################################################################
# Usando a analise de velocidades para empilhar o dado 
##################################################################

sunmo <$CDP_data par=$velocities | sustack | sustolt \
par=$velocities cdpmin=$cdp_min cdpmax=$cdp_max dxcdp=$dcdp \
>$STOLT_data
