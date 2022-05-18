#%% Importando bibliotecas

import sys
import utm
import numpy as np
import cartopy.crs as ccrs
import matplotlib.pyplot as plt
import cartopy.feature as cfeature
import matplotlib.ticker as mticker
import matplotlib.animation as animation
from cartopy.mpl.gridliner import LATITUDE_FORMATTER,LONGITUDE_FORMATTER

#%% Lendo arquivos

prefixo = "../../parameters/"
src = np.loadtxt(prefixo + "source_UTM_coordinates.txt",dtype=str)
rec = np.loadtxt(prefixo + "receiver_UTM_coordinates.txt",dtype=str)
fldr = np.loadtxt(prefixo + "FFID.txt",dtype=str)

#%% Inicializando variaveis para a conversão str-float/int

ffid = np.zeros(len(fldr))
src_UTME = np.zeros(len(ffid))
src_UTMN = np.zeros(len(ffid))
rec_UTME = np.zeros(len(ffid))
rec_UTMN = np.zeros(len(ffid))

#%% Convertendo arquivos de str para float / int

for i in range(len(ffid)):
    
    src_UTME[i] = float(src[i][0][3:]) / 100
    src_UTMN[i] = float(src[i][1][3:]) / 100

    rec_UTME[i] = float(rec[i][0][3:]) / 100
    rec_UTMN[i] = float(rec[i][1][3:]) / 100

    ffid[i] = int(fldr[i][5:])

#%% Excluindo arquivos da memoria

del src
del rec
del fldr

#%% Coletando o número de receptores por tiro 

cont = 0
tracesPerShot = np.array([],dtype=int)
for i in range(1,len(ffid)):
    cont += 1
    if ffid[i] != ffid[i-1]:
        tracesPerShot = np.append(tracesPerShot,cont)
        cont = 0

tracesPerShot = np.append(tracesPerShot,cont)

#%% Plot individual da geometria (shot + conjunto de receptores) em UTM

nrec = tracesPerShot[0]
src_UTME = src_UTME[::nrec] # start:stop:step
src_UTMN = src_UTMN[::nrec]

# shot = 1
# for i in range(len(tracesPerShot)):
#     # plt.scatter(rec_UTME[int(i*nrec):int((i+1)*nrec)],rec_UTMN[int(i*nrec):int((i+1)*nrec)])
#     plt.scatter(src_UTME[i],src_UTMN[i])

# plt.show()

#%% Convertendo de UTM para LatLon

src_LAT = np.array([ ]) 
src_LON = np.array([ ])
rec_LAT = np.array([ ]) 
rec_LON = np.array([ ])

for i in range(len(tracesPerShot)):    
    transformed_src = utm.to_latlon(src_UTME[i],src_UTMN[i],30,'U')

    src_LAT = np.append(transformed_src[0],src_LAT)
    src_LON = np.append(transformed_src[1],src_LON)

#%% Plot individual da geometria (shot + conjunto de receptores) em Lat Lon

# for i in range(len(tracesPerShot)):

#     plt.scatter(src_LON[i],src_LAT[i])

# plt.show()    

#%% Plotando a aquisição no mapa (Tentar ajeitar o mapa para UTM)

fig = plt.figure(figsize=(6,6))

ax = fig.add_subplot(111,projection=ccrs.PlateCarree())

ax.add_feature(cfeature.LAND)
ax.add_feature(cfeature.OCEAN)
ax.add_feature(cfeature.COASTLINE)
ax.add_feature(cfeature.BORDERS)
ax.add_feature(cfeature.RIVERS)

lon_O = -15
lon_L =  3
lat_N =  60
lat_S =  50

ax.set_extent([lon_O,lon_L,lat_N,lat_S],ccrs.PlateCarree())

# Adicionando todos os pontos de tiro
for i in range(len(tracesPerShot)):
    plt.scatter(src_LON[i],src_LAT[i],s=50,color='red',transform=ccrs.PlateCarree())

# Adicionando legendas à figura
labels = ["Pontos de tiro"]
plt.figlegend(labels, bbox_to_anchor=(0.420, 0.71))

# Inserindo linhas de grade
g1 = ax.gridlines(ccrs.PlateCarree(),draw_labels=True,linestyle='--',linewidth=0.5)
g1.right_labels = False  # Latitudes
g1.top_labels = False    # Longitudes

# Adicionando Titulo e nome dos eixos
ax.set_title("Localização da aquisição sísmica da Costa Oeste da Inglaterra")
ax.set_ylabel("Longitude",fontsize=10)
ax.set_xlabel("Latitude",fontsize=10)

# Deixando as linhas de grade na mesma escala
# g1.ylocator = mticker.FixedLocator(np.arange(lat_S,lat_N+5,10))

# Modificando aspecto nos eixos
g1.yformatter = LATITUDE_FORMATTER
g1.xformatter = LONGITUDE_FORMATTER

g1.xlabel_style = {'size':10}
g1.ylabel_style = {'size':10}

plt.savefig('area_de_estudo.png',dpi=300,bbox_inches='tight')
plt.show()

#%% Fazendo animação do comportamento dos receptores por tiro

# fig = plt.figure(figsize=(6,6))

# ims = []
# for i in range(len(tracesPerShot)):

#     nrec = tracesPerShot[i]

#     im = plt.scatter(rec_UTME[int(i*nrec):int((i+1)*nrec)],rec_UTMN[int(i*nrec):int((i+1)*nrec)])
#     ims.append([im])

# ani = animation.ArtistAnimation(fig,ims, interval=10, blit=True, repeat=True)

# writer = animation.FFMpegWriter(fps=15, metadata=dict(artist='Me'), bitrate=1800)

# plt.title(f"Movimentação do arranjo End-On para os {len(tracesPerShot)} tiros")
# plt.xlabel("UTM Leste")
# plt.ylabel("UTM Norte")

# ani.save("movimenta.mp4", writer=writer)

# plt.show()
