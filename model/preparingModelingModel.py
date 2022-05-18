import sys
import numpy as np
import matplotlib.pyplot as plt

def readbinaryfile(dim1,dim2,filename):
    with open(filename, 'rb') as f:    
        data   = np.fromfile(filename, dtype= np.float32, count= dim1*dim2)
        matrix = np.reshape(data, [dim1,dim2], order='C')
    return matrix

nxr = 2772
nzr = 323

modelEngland = readbinaryfile(nzr,nxr,f"vpAbrupto.bin") 
smooth = readbinaryfile(nxr,nzr,"vint_final_corr.bin").T

nx = 2*nxr
nz = 323    

dx = 6.250
# dz = 6.1919
dz = 6.658

vp = np.zeros((nz,nx))
vs = np.zeros((nz,nx))
rho = np.zeros((nz,nx))
vpTrue = np.zeros((nz,nx))

vp[:,::2] = modelEngland
vp[:,-1] = modelEngland[:,-1]

vpTrue[:,::2] = smooth
vpTrue[:,-1] = smooth[:,-1]

for i in range(1,nx-1,2):
    vp[:,i] = (vp[:,i-1] + vp[:,i+1]) / 2.0
    vpTrue[:,i] = (vpTrue[:,i-1] + vpTrue[:,i+1]) / 2.0

for j in range(nx):
    for i in range(nz): 
        vs[i,j] = vp[i,j] / np.sqrt(3.0)        
        rho[i,j] = 310.0 * pow(vp[i,j],0.25)

        if(vp[i,j] == 1500):
            vs[i,j] = 0.0
            rho[i,j] = 1000.0 

zloc = np.linspace(0,nz,5)
zlab = np.round(zloc * dz, decimals = 1)

xloc = np.linspace(0,nx,11)
xlab = np.round(xloc * dx, decimals = 1)

plt.figure(1,figsize=(15,14))
plt.subplot(311)
plt.imshow(vpTrue,aspect="auto")
plt.xticks(xloc,np.array(xlab,dtype=int))
plt.yticks(zloc,np.array(zlab,dtype=int))
cbar = plt.colorbar()
cbar.set_label("Velocidades P [m/s]",fontsize=15)
plt.ylabel("Profundidade [m]",fontsize=15)
plt.title("Modelo de velocidade compressional",fontsize=20)

plt.subplot(312)
plt.imshow(vs,aspect="auto")
plt.xticks(xloc,np.array(xlab,dtype=int))
plt.yticks(zloc,np.array(zlab,dtype=int))
cbar = plt.colorbar()
cbar.set_label("Velocidades S [m/s]",fontsize=15)
plt.ylabel("Profundidade [m]",fontsize=15)
plt.title("Modelo de velocidade cisalhante",fontsize=20)

plt.subplot(313)
plt.imshow(rho,aspect="auto")
plt.xticks(xloc,np.array(xlab,dtype=int))
plt.yticks(zloc,np.array(zlab,dtype=int))
cbar = plt.colorbar()
cbar.set_label("Densidades [kg/m³]",fontsize=15)
plt.xlabel("Distância [m]",fontsize=15)
plt.ylabel("Profundidade [m]",fontsize=15)
plt.title("Modelo de densidade",fontsize=20)

plt.savefig("ModelosInput_Corr.png",dpi=200,bbox_inches="tight")
plt.show()

vpTrue.astype("float32",order="C").tofile(f"vpModelEngland.bin")
vs.astype("float32",order="C").tofile(f"vsModelEngland.bin")
rho.astype("float32",order="C").tofile(f"rhoModelEngland.bin")
