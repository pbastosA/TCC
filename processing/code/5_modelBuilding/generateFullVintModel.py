import sys
import numpy as np
import matplotlib.pyplot as plt

def readbinaryfile(dim1,dim2,filename):
    data   = np.fromfile(filename, dtype= np.float32, count= dim1*dim2)
    matrix = np.reshape(data, [dim1,dim2], order='C')
    return matrix.T

def readHorizon(dim,filename):
    data = np.fromfile(filename, dtype=np.int32, count=dim)

    return data

nx = 1810
nz = 501
dt = 0.004
dx = 12.5

RMSmodel = readbinaryfile(nx,nz,"vrms_cmps_completos_smooth.bin")

t = np.arange(nz) * dt

INTmodel = np.zeros((nz,nx))
INTmodel[0,0] = RMSmodel[0,0]

for j in range(nx):
    for i in range(1,nz):
        INTmodel[i,j] = np.sqrt((RMSmodel[i,j]**2 * t[i] - RMSmodel[i-1,j]**2 * t[i-1]) / (t[i] - t[i-1]))

i,j = np.where(INTmodel == 0.0)
INTmodel[i,j] = 1500.0

nxr = 2772
nzr = 340

shadow = 638 

hrz1 = np.array([readHorizon(1810,"hrzs/xhrz0_1810ams.bin")+shadow,readHorizon(1810,"hrzs/zhrz0.bin")])
hrz2 = np.array([readHorizon(1810,"hrzs/xhrz1_1810ams.bin")+shadow,readHorizon(1810,"hrzs/zhrz1.bin")])
hrz3 = np.array([readHorizon(1810,"hrzs/xhrz2_1810ams.bin")+shadow,readHorizon(1810,"hrzs/zhrz2.bin")])
hrz4 = np.array([readHorizon(1482,"hrzs/xhrz3_1482ams.bin")+shadow,readHorizon(1482,"hrzs/zhrz3.bin")])
hrz5 = np.array([readHorizon(1568,"hrzs/xhrz4_1568ams.bin")+shadow,readHorizon(1568,"hrzs/zhrz4.bin")])
hrz6 = np.array([readHorizon(1810,"hrzs/xhrz5_1810ams.bin")+shadow,readHorizon(1810,"hrzs/zhrz5.bin")])
hrz7 = np.array([readHorizon(1392,"hrzs/xhrz6_1392ams.bin")+shadow,readHorizon(1392,"hrzs/zhrz6.bin")])
hrz8 = np.array([readHorizon(1810,"hrzs/xhrz7_1810ams.bin")+shadow,readHorizon(1810,"hrzs/zhrz7.bin")])

h1 = np.zeros((nxr,2))
h2 = np.zeros((nxr,2))
h3 = np.zeros((nxr,2))
h6 = np.zeros((nxr,2))
h8 = np.zeros((nxr,2))

h4 = np.zeros((shadow+1482,2))
h5 = np.zeros((shadow+1568,2))

h7 = hrz7

for i in range(shadow):
    h1[i,0] = i; h1[i,1] = hrz1[1][0]
    h2[i,0] = i; h2[i,1] = hrz2[1][0]
    h3[i,0] = i; h3[i,1] = hrz3[1][0]
    h4[i,0] = i; h4[i,1] = hrz4[1][0]
    h5[i,0] = i; h5[i,1] = hrz5[1][0]
    h6[i,0] = i; h6[i,1] = hrz6[1][0]
    h8[i,0] = i; h8[i,1] = hrz8[1][0]

for i in range(nx+shadow,nxr):
    h1[i,0] = i; h1[i,1] = hrz1[1][-1]
    h2[i,0] = i; h2[i,1] = hrz2[1][-1]
    h3[i,0] = i; h3[i,1] = hrz3[1][-1]
    h6[i,0] = i; h6[i,1] = hrz6[1][-1]
    h8[i,0] = i; h8[i,1] = hrz8[1][-1]

h1[shadow:nx+shadow,0] = hrz1[0][:]; h1[shadow:nx+shadow,1] = hrz1[1][:]
h2[shadow:nx+shadow,0] = hrz2[0][:]; h2[shadow:nx+shadow,1] = hrz2[1][:]
h3[shadow:nx+shadow,0] = hrz3[0][:]; h3[shadow:nx+shadow,1] = hrz3[1][:]
h4[shadow:shadow+1482,0] = hrz4[0][:]; h4[shadow:shadow+1482,1] = hrz4[1][:] 
h5[shadow:shadow+1569,0] = hrz5[0][:]; h5[shadow:shadow+1569,1] = hrz5[1][:]
h6[shadow:nx+shadow,0] = hrz6[0][:]; h6[shadow:nx+shadow,1] = hrz6[1][:]
h8[shadow:nx+shadow,0] = hrz8[0][:]; h8[shadow:nx+shadow,1] = hrz8[1][:]

locks_t = np.linspace(0,nz,11)
labels_t = np.around(locks_t * dt,decimals=1)

locks_x = np.linspace(0,nx,7)
labels_x = np.linspace(0,nx,7,dtype=int)

# Modelo RMS suavizado
# plt.figure(1,figsize=(15,5))
# plt.imshow(RMSmodel,aspect="auto")
# cbar = plt.colorbar()
# cbar.set_label("Velocidade RMS [m/s]",fontsize=15)
# plt.title("Modelo RMS suavizado",fontsize=20)
# plt.xlabel("CMPs",fontsize=15)
# plt.ylabel("Tempo [s]",fontsize=15)
# plt.yticks(locks_t,labels_t)
# plt.xticks(locks_x,labels_x)
# plt.savefig("modeloSuavizadoRMS.png",dpi=200,bbox_inches="tight")

# Modelo centralizado na geometria
# plt.figure(2,figsize=(15,5))
# plt.imshow(INTmodel[:,:],aspect="auto")
# cbar = plt.colorbar()
# cbar.set_label("Velocidade intervalar [m/s]",fontsize=15)
# plt.title("Modelo intervalar resultante",fontsize=20)
# plt.xlabel("CMPs",fontsize=15)
# plt.ylabel("Tempo [s]",fontsize=15)
# plt.yticks(locks_t,labels_t)
# plt.xticks(locks_x,labels_x)
# plt.savefig("modeloSuavizadoINT.png",dpi=200,bbox_inches="tight")

# plt.show()
# sys.exit()
# outputVint = INTmodel.T
# outputVint.astype("float32",order="C").tofile("vintCMPs.bin")

ultraModel = np.zeros((nzr,nxr)) * np.nan
ultraModel[:,shadow:nx+shadow] = INTmodel[:nzr,:]

locks_t = np.linspace(0,nzr,5)
labels_t = np.around(locks_t * dt,decimals=1)

locks_x = np.linspace(0,nxr,7)
labels_x = np.linspace(0,nxr*dx,7,dtype=int)

# Modelo preenchido completamente
# plt.figure(3,figsize=(15,5))
# plt.imshow(ultraModel,aspect="auto")
# cbar = plt.colorbar()
# cbar.set_label("Velocidade intervalar [m/s]",fontsize=15)
# plt.title("Modelo intervalar encaixado",fontsize=20)
# plt.xlabel("Distância [m]",fontsize=15)
# plt.ylabel("Tempo [s]",fontsize=15)
# plt.yticks(locks_t,labels_t)
# plt.xticks(locks_x,labels_x)
# plt.savefig("modeloReduzidoINT.png",dpi=200,bbox_inches="tight")

for i in range(shadow):
    ultraModel[:,i] = INTmodel[:nzr,0]

for i in range(nx+shadow,nxr):    
    ultraModel[:,i] = INTmodel[:nzr,-1]

modelCorr = ultraModel.copy()
for j in range(len(ultraModel[0])):
    for i in range(int(h1[j,1]),len(ultraModel)):
        modelCorr[i,j] += 1000 - i*2.8

diffModel = np.abs(modelCorr - ultraModel)

plt.figure(4,figsize=(15,14))
plt.subplot(311)
plt.imshow(ultraModel,aspect="auto")
cbar = plt.colorbar()
cbar.set_label("Velocidade P [m/s]",fontsize=15)
plt.ylabel("Tempo [s]",fontsize=15)
plt.title("Modelo estimado inicial",fontsize=20)
plt.yticks(locks_t,labels_t)
plt.xticks(locks_x,labels_x)

plt.subplot(312)
plt.imshow(modelCorr,aspect="auto")
plt.yticks(locks_t,labels_t)
plt.xticks(locks_x,labels_x)
cbar = plt.colorbar()
plt.title("Modelo modificado",fontsize=20)
cbar.set_label("Velocidade P [m/s]",fontsize=15)
plt.ylabel("Tempo [s]",fontsize=15)

plt.subplot(313)
plt.imshow(diffModel,aspect="auto")
plt.yticks(locks_t,labels_t)
plt.xticks(locks_x,labels_x)
cbar = plt.colorbar()
cbar.set_label("Gradiente linear [m/s]",fontsize=15)
plt.title("Diferença entre os modelos",fontsize=20)
plt.ylabel("Tempo [s]",fontsize=15)
plt.xlabel("Distância [m]",fontsize=15)

plt.savefig("modificationTime.png",dpi=200,bbox_inches="tight")
print(np.shape(modelCorr))

modelCorr = modelCorr.T
modelCorr.astype("float32",order="C").tofile("vint_final_inTime.bin")

plt.show()
sys.exit()

prof1 = []
prof2 = []
for j in range(1):
    p1 = 0
    p2 = 0
    for i in range(nzr):
        p1 += dt*ultraModel[i,0]/2
        p2 += dt*modelCorr[i,0]/2
    
    prof1.append(int(p1))
    prof2.append(int(p2))

dz_model1 = sum(prof1)/len(prof1)/nzr
dz_model2 = sum(prof2)/len(prof2)/nzr

dz_model1 = 6.19195
dz_model2 = 6.658

offset = 100.0
velpwb = 1500.0

hwb_prof = np.sqrt((0.5*offset)**2 + (0.5*velpwb*h1[:,1]*dt)**2)  

delay = int(np.min(h1[:,1]) - np.min(np.array(hwb_prof/dz_model2,dtype=int)))

nzr -= delay
ultraModel = ultraModel[delay:,:]
modelCorr  = modelCorr[delay:,:]
diffModel  = diffModel[delay:,:]

h1[:,1] -= delay
h2[:,1] -= delay
h3[:,1] -= delay
h4[:,1] -= delay
h5[:,1] -= delay
h6[:,1] -= delay
hrz7[1] -= delay
h8[:,1] -= delay

for i in range(len(hwb_prof)):
    # ultraModel[:int(hwb_prof[i]/dz_model2),:] = 1500.0
    modelCorr[:int(hwb_prof[i]/dz_model2),:] = 1500.0
    diffModel[:int(hwb_prof[i]/dz_model2),:] = 0.0

print(f"nx   = {len(ultraModel[0])}")
print(f"nz   = {len(ultraModel)}")
print(f"prof = {nzr*dz_model1:.0f} {nzr*dz_model2:.0f}")
print(f"dzs  = {dz_model1:.3f} {dz_model2:.3f}")

locks_z = np.linspace(0,nzr,5,dtype=int)

label1_z = np.linspace(0,nzr*dz_model1+1,5,dtype=int)
label2_z = np.linspace(0,nzr*dz_model2,5,dtype=int)

plt.figure(5,figsize=(15,14))
plt.subplot(311)
plt.imshow(ultraModel,aspect="auto")
cbar = plt.colorbar()
cbar.set_label("Velocidade P [m/s]",fontsize=15)
plt.ylabel("Profundidade [m]",fontsize=15)
plt.title("Modelo estimado inicial",fontsize=20)
plt.yticks(locks_z,label1_z)
plt.xticks(locks_x,labels_x)

plt.subplot(312)
plt.imshow(modelCorr,aspect="auto")
plt.yticks(locks_z,label2_z)
plt.xticks(locks_x,labels_x)
cbar = plt.colorbar()
plt.title("Modelo modificado",fontsize=20)
cbar.set_label("Velocidade P [m/s]",fontsize=15)
plt.ylabel("Profundidade [m]",fontsize=15)

plt.subplot(313)
plt.imshow(diffModel,aspect="auto")
plt.xticks(locks_x,labels_x)
cbar = plt.colorbar()
cbar.set_label("Gradiente linear [m/s]",fontsize=15)
plt.title("Diferença entre os modelos",fontsize=20)
plt.ylabel("Ampstras na vertical",fontsize=15)
plt.xlabel("Distância [m]",fontsize=15)

plt.savefig("modificationDepth.png",dpi=200,bbox_inches="tight")


# plt.figure(6,figsize=(15,5))
# plt.imshow(ultraModel,aspect="auto")
# cbar = plt.colorbar()
# cbar.set_label("Velocidade intervalar [m/s]",fontsize=15)
# plt.title("Modelo intervalar extrapolado em profundidade",fontsize=20)
# plt.xlabel("Distância [m]",fontsize=15)
# plt.ylabel("Profundidade [m]",fontsize=15)

# plt.scatter(h1[:,0],h1[:,1],marker=".")
# plt.scatter(h2[:,0],h2[:,1],marker=".")
# plt.scatter(h3[:,0],h3[:,1],marker=".")
# plt.scatter(h4[:,0],h4[:,1],marker=".")
# plt.scatter(h5[:,0],h5[:,1],marker=".")
# plt.scatter(h6[:,0],h6[:,1],marker=".")
# plt.scatter(hrz7[0],hrz7[1],marker=".")
# plt.scatter(h8[:,0],h8[:,1],marker=".",c="lightblue")

# plt.yticks(locks_z,label1_z)
# plt.xticks(locks_x,labels_x)

# plt.savefig("modeloExtrapoladoINTHRZ.png",dpi=200,bbox_inches="tight")
# plt.tight_layout()
plt.show()

ultraModel = ultraModel.T
ultraModel.astype("float32",order="C").tofile("vint_final_old.bin")

modelCorr = modelCorr.T
modelCorr.astype("float32",order="C").tofile("vint_final_corr.bin")

