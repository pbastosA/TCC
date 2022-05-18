import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

def readbinaryfile(dim1,dim2,filename):
    data   = np.fromfile(filename, dtype= np.float32, count= dim1*dim2)
    matrix = np.reshape(data, [dim1,dim2], order='C')
    return matrix.T

def readHorizon(dim,filename):
    data = np.fromfile(filename, dtype=np.int32, count=dim)
    return data

nx1 = 2772
nz1 = 340 

dt = 0.004

shadow = 638 

hrz1 = np.array([readHorizon(1810,"hrzs/xhrz0_1810ams.bin")+shadow,readHorizon(1810,"hrzs/zhrz0.bin")])
hrz2 = np.array([readHorizon(1810,"hrzs/xhrz1_1810ams.bin")+shadow,readHorizon(1810,"hrzs/zhrz1.bin")])
hrz3 = np.array([readHorizon(1810,"hrzs/xhrz2_1810ams.bin")+shadow,readHorizon(1810,"hrzs/zhrz2.bin")])
hrz4 = np.array([readHorizon(1482,"hrzs/xhrz3_1482ams.bin")+shadow,readHorizon(1482,"hrzs/zhrz3.bin")])
hrz5 = np.array([readHorizon(1568,"hrzs/xhrz4_1568ams.bin")+shadow,readHorizon(1568,"hrzs/zhrz4.bin")])
hrz6 = np.array([readHorizon(1810,"hrzs/xhrz5_1810ams.bin")+shadow,readHorizon(1810,"hrzs/zhrz5.bin")])
hrz7 = np.array([readHorizon(1392,"hrzs/xhrz6_1392ams.bin")+shadow,readHorizon(1392,"hrzs/zhrz6.bin")])
hrz8 = np.array([readHorizon(1810,"hrzs/xhrz7_1810ams.bin")+shadow,readHorizon(1810,"hrzs/zhrz7.bin")])

nx = 1810

h1 = np.zeros((nx1,2))
h2 = np.zeros((nx1,2))
h3 = np.zeros((nx1,2))
h6 = np.zeros((nx1,2))
h8 = np.zeros((nx1,2))

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

for i in range(nx+shadow,nx1):
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

vintCorr = readbinaryfile(nx1,nz1,"vint_final_inTime.bin")  

rects = []
picks = np.arange(642,2443,180,dtype=int)

for i in range(len(picks)):
    rects.append(Rectangle((picks[i],0),0.001,nz1-1,linewidth=1,edgecolor='r',facecolor='none'))

locks_z = np.linspace(0,nz1,5,dtype=int)
label_z = locks_z * dt

locks_x = np.linspace(0,nx1,11,dtype=int)
label_x = np.array(np.linspace(0,nx1*12.5,11),dtype=int)

plt.figure(1,figsize=(15,5))
plt.imshow(vintCorr,aspect="auto",cmap="Greys")
cbar = plt.colorbar()
cbar.set_label("Velocidade intervalar [m/s]",fontsize=12)
plt.title("Modelo corrigido com horizontes e marcações projetadas",fontsize=15)
plt.ylabel("Tempo [s]",fontsize=14)
plt.xlabel("Distância [m]",fontsize=14)

for i in range(len(picks)):
    plt.gca().add_patch(rects[i])

plt.scatter(h1[:,0],h1[:,1],marker=".")
plt.scatter(h2[:,0],h2[:,1],marker=".")
plt.scatter(h3[:,0],h3[:,1],marker=".")
plt.scatter(h4[:,0],h4[:,1],marker=".")
plt.scatter(h5[:,0],h5[:,1],marker=".")
plt.scatter(h6[:,0],h6[:,1],marker=".")
plt.scatter(hrz7[0],hrz7[1],marker=".")
plt.scatter(h8[:,0],h8[:,1],marker=".",c="lightblue")

plt.yticks(locks_z,label_z)
plt.xticks(locks_x,label_x)

plt.tight_layout()
plt.savefig("teste.png",bbox_inches="tight",dpi=200)
plt.show()

#######################################################################################

vintPick = vintCorr[:,picks]

vrmsCal = np.zeros((nz1,11))

dts = np.ones(len(vintPick)) * dt

#velocidade intervalar para velocidade RMS
for j in range(len(picks)):
    vrmsCal[0,j] = vintPick[0,j]
    for i in range(len(vintPick)):
        sv2t = vintPick[:i+1,j]**2 * dts[:i+1]
        st = dts[:i+1]
        
        vrmsCal[i,j] = np.sqrt(sum(sv2t) / sum(st))

nx2 = 1810 
nz2 = 501

vrmsObs = readbinaryfile(nx2,nz2,"vrms_cmps_completos_smooth.bin")[:nz1,:]

time = np.arange(nz1) * dt

plt.figure(2,figsize=(20,7))

for i in range(len(picks)):
    plt.subplot(1,11,i+1)

    plt.plot(vrmsObs[:,i],time)
    plt.plot(vrmsCal[:,i],time)

    plt.gca().invert_yaxis()

plt.tight_layout()
plt.show()

v = np.around(vrmsCal[::35],decimals=5)
t = np.around(time[::35],decimals=5)

vpick = open("vpick_corrigido.txt","w")
vpick.write("cdp=9943,10303,10663,11023,11383,11743,12103,12463,12823,13183,13561 \ \n")
vpick.write("#=1,2,3,4,5,6,7,8,9,10,11 \ \n")

for i in range(len(picks)):
    vpick.write(f"tnmo={t[0]},{t[1]},{t[2]},{t[3]},{t[4]},{t[5]},{t[6]},{t[7]},{t[8]},{t[9]} \ \n")
    vpick.write(f"vnmo={v[0,i]},{v[1,i]},{v[2,i]},{v[3,i]},{v[4,i]},{v[5,i]},{v[6,i]},{v[7,i]},{v[8,i]},{v[9,i]} \ \n")

vpick.close()