import numpy as np
import matplotlib.pyplot as plt

def readbinaryfile(dim1,dim2,filename):
    with open(filename, 'rb') as f:    
        data   = np.fromfile(filename, dtype= np.float32, count= dim1*dim2)
        matrix = np.reshape(data, [dim1,dim2], order='C')
    return matrix.T

#%% Plotando espectros de amplitude

dt = 0.004
spread = 160
nt = 1261

f = np.array([0,0,20,40,60,80,100,120])

flt_ampSpec = readbinaryfile(spread,nt,"CMP10123/espectro_amplitude_flt.bin")
raw_ampSpec = readbinaryfile(spread,nt,"CMP10123/espectro_amplitude_raw.bin")
mig_ampSpec = readbinaryfile(spread,nt,"CMP10123/espectro_amplitude_mig.bin")

cont = 0
images = np.array([flt_ampSpec,raw_ampSpec,mig_ampSpec])

fig, axes = plt.subplots(ncols=3,nrows=1,dpi=150)
fig.set_size_inches(10,8)

axes[0].set_title("Espectro - MGFLT")
axes[0].set_ylabel("Frequências [Hz]",fontsize=15)
axes[0].set_xlabel("Traços",fontsize=15)
axes[0].set_yticklabels(f)    

axes[1].set_title("Espectro - MGRAW")
axes[1].set_yticklabels([])
axes[1].set_xlabel("Traços",fontsize=15)

axes[2].set_title("Espectro - PREMIG")
axes[2].set_yticklabels([])
axes[2].set_xlabel("Traços",fontsize=15)

for ax in axes.flat:
    im = ax.imshow(images[cont],aspect="auto",cmap="Greys")
    cont += 1

cbar = fig.colorbar(im,aspect="auto",cmap="Greys",ax=axes.flat,fraction=0.025)
cbar.set_label("Amplitude",fontsize = 15, rotation = 90)

plt.savefig("amp_spec.png",dpi=200,bbox_inches='tight')
plt.show()

#%% Plotando espectros de fase

flt_faseSpec = readbinaryfile(spread,nt,"CMP10123/espectro_fase_flt.bin")
raw_faseSpec = readbinaryfile(spread,nt,"CMP10123/espectro_fase_raw.bin")
mig_faseSpec = readbinaryfile(spread,nt,"CMP10123/espectro_fase_mig.bin")

cont = 0
images = np.array([flt_faseSpec,raw_faseSpec,mig_faseSpec])

fig, axes = plt.subplots(ncols=3,nrows=1,dpi=150)
fig.set_size_inches(10,8)

axes[0].set_title("Espectro - MGFLT")
axes[0].set_ylabel("Frequências [Hz]",fontsize=15)
axes[0].set_xlabel("Traços",fontsize=15)
axes[0].set_yticklabels(f)    

axes[1].set_title("Espectro - MGRAW")
axes[1].set_yticklabels([])
axes[1].set_xlabel("Traços",fontsize=15)

axes[2].set_title("Espectro - PREMIG")
axes[2].set_yticklabels([])
axes[2].set_xlabel("Traços",fontsize=15)

for ax in axes.flat:
    im = ax.imshow(images[cont],aspect="auto",cmap="Greys")
    cont += 1

cbar = fig.colorbar(im,aspect="auto",cmap="Greys",ax=axes.flat,fraction=0.025)
cbar.set_label("Fase",fontsize = 15, rotation = 90)

ticks = ["-172°","-115°","-60°","0°","60°","115°","172°"]
cbar.ax.set_yticklabels(ticks)

plt.savefig("fase_spec.png",dpi=200,bbox_inches='tight')
plt.show()






