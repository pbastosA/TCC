import sys
import numpy as np
import matplotlib.pyplot as plt


def readHorizon(dim,filename):
    with open(filename, 'rb') as f:    
        data = np.fromfile(filename, dtype=np.int32, count=dim)

    return data

nx = 1810

nxr = 2772
nzr = 340

dx = 12.50
# dz = 6.658
dz = 6.173
dt = 0.004

shadow = 641 

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

h7 = np.zeros((1392,2))

h7[:,0] = hrz7[0]; h7[:,1] = hrz7[1] 

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

offset = 100.0
velpwb = 1500.0

hwb_prof = np.sqrt((0.5*offset)**2 + (0.5*velpwb*h1[:,1]*dt)**2)  

delay = int(np.min(h1[:,1]) - np.min(np.array(hwb_prof/dz,dtype=int)))

nzr -= delay

h1[:,1] -= delay
h2[:,1] -= delay
h3[:,1] -= delay
h4[:,1] -= delay
h5[:,1] -= delay
h6[:,1] -= delay
h7[:,1] -= delay
hrz7[1] -= delay
h8[:,1] -= delay

modelEngland = np.zeros((nzr,nxr))

velocities = [1500,1800,2100,2500,2900,3100,3500,3900,4300]
# velocities = [1500,2700,3000,3100,3500,3900,4100,4300,4600]

for j in range(nxr):
    for i in range(int(h1[j,1])):
        modelEngland[i,j] = velocities[0]

    for i in range(int(h1[j,1]),int(h2[j,1])+1):
        modelEngland[i,j] = velocities[1]

    for i in range(int(h2[j,1]),int(h3[j,1])+1):
        modelEngland[i,j] = velocities[2]

    for i in range(int(h8[j,1]),nzr):
        modelEngland[i,j] = velocities[8]

for j in range(shadow+1482):
    for i in range(int(h3[j,1]),int(h4[j,1])+1):
        modelEngland[i,j] = velocities[3]

    for i in range(int(h4[j,1]),int(h5[j,1])+1):
        modelEngland[i,j] = velocities[4]

for j in range(shadow+1482,shadow+1568):
    for i in range(int(h3[j,1]),int(h5[j,1])+1):
        modelEngland[i,j] = velocities[4]

for j in range(shadow+1568):
    for i in range(int(h5[j,1]),int(h6[j,1])+1):
        modelEngland[i,j] = velocities[5]

for j in range(shadow+1568,nxr):
    for i in range(int(h3[j,1]),int(h6[j,1])+1):
        modelEngland[i,j] = velocities[5]

for j in range(743):
    for i in range(int(h6[j,1]),int(h8[j,1])+1):
        modelEngland[i,j] = velocities[6]

for j in range(1974,2045):
    for i in range(int(h6[j,1]),int(h8[j,1])+1):
        modelEngland[i,j] = velocities[6]

count = 0
for j in range(743,1974):
    for i in range(int(h6[j,1]),int(h7[count,1])+1):
        modelEngland[i,j] = velocities[6]

    for i in range(int(h7[count,1]),int(h8[j,1])+1):
        modelEngland[i,j] = velocities[7]

    count += 1

for j in range(2045,2203):
    for i in range(int(h6[j,1]),int(h7[count+1,1])+1):
        modelEngland[i,j] = velocities[6]

    for i in range(int(h7[count,1]),int(h8[j,1])+1):
        modelEngland[i,j] = velocities[7]

    count += 1

for j in range(2203,nxr):
    for i in range(int(h6[j,1])+1,int(h8[j,1])+1):
        modelEngland[i,j] = velocities[6]

i,j = np.where(modelEngland == 0)
modelEngland[i,j] = velocities[7]

zloc = np.linspace(0,nzr,5)
zlab = np.round(zloc * dz, decimals = 1)

xloc = np.linspace(0,nxr,11)
xlab = np.round(xloc * dx, decimals = 1)

plt.figure(1,figsize=(15,5))

plt.imshow(modelEngland,aspect="auto")
cbar = plt.colorbar()
cbar.set_label("Velocidades médias [m/s]",fontsize=15)
plt.xlabel("Distância [m]",fontsize=15)
plt.ylabel("Profundidade [m]",fontsize=15)
plt.title("Velocidade constante por horizonte",fontsize=20)

plt.scatter(h1[:,0],h1[:,1],marker=".")
plt.scatter(h2[:,0],h2[:,1],marker=".")
plt.scatter(h3[:,0],h3[:,1],marker=".")
plt.scatter(h4[:,0],h4[:,1],marker=".")
plt.scatter(h5[:,0],h5[:,1],marker=".")
plt.scatter(h6[:,0],h6[:,1],marker=".")
plt.scatter(hrz7[0],hrz7[1],marker=".")
plt.scatter(h8[:,0],h8[:,1],marker=".",c="lightblue")

plt.xticks(xloc,np.array(xlab,dtype=int))
plt.yticks(zloc,np.array(zlab,dtype=int))
plt.tight_layout()

plt.savefig("modeloAbrupto.png",dpi=200,bbox_inches="tight")
plt.show()

modelEngland.astype("float32",order="C").tofile(f"vpAbrupto.bin")
