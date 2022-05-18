import sys
import numpy as np
import matplotlib.pyplot as plt

def readbinaryfile(dim1,dim2,filename):
    with open(filename, 'rb') as f:    
        data   = np.fromfile(filename, dtype= np.float32, count= dim1*dim2)
        matrix = np.reshape(data, [dim1,dim2], order='C')
    return matrix.T

nx = 2772
nz = 501

dt = 0.004
dz = 6.0
dx = 12.5

ncdp = 1810

vint = readbinaryfile(nx,nz,"vint_final.bin")
vrms = readbinaryfile(ncdp,nz,"vrms_cmps_completos_smooth.bin")

plt.figure(1,figsize=(35,15))

plt.subplot(211)
ylocks = np.linspace(0,nz-1,7) 
ylabel = np.round(np.linspace(0,nz-1,7) * dt,decimals=1)
plt.imshow(vrms,aspect="auto")
plt.yticks(ylocks,ylabel)
cbar = plt.colorbar()
cbar.set_label("Velocidade RMS [m/s]",fontsize=15)
plt.title("Modelo de velocidades RMS",fontsize=20)
plt.xlabel("CMPs completos do dado",fontsize=15)
plt.ylabel("Tempo [s]",fontsize=15)

plt.subplot(212)
xlocks = np.linspace(0,nx,11) 
xlabel = np.round(np.linspace(0,nx,11) * dx,decimals=1)
ylocks = np.linspace(0,nz-1,7) 
ylabel = np.linspace(0,nz-1,7) * dz
plt.imshow(vint,aspect="auto")
plt.xticks(xlocks,xlabel)
plt.yticks(ylocks,ylabel)
cbar = plt.colorbar()
cbar.set_label("Velocidade Intervalar [m/s]",fontsize=15)
plt.title("Modelo de velocidades intervalares",fontsize=20)
plt.xlabel("Distância [m]",fontsize=15)
plt.ylabel("Profundidade [m]",fontsize=15)

plt.savefig("modelosRMSINT.png",dpi=200,bbox_inches="tight")
plt.show()



