import sys
from skimage import exposure
import numpy as np
import matplotlib.pyplot as plt

def readbinaryfile(dim1,dim2,filename):
    with open(filename, 'rb') as f:    
        data   = np.fromfile(filename, dtype= np.float32, count= dim1*dim2)
        matrix = np.reshape(data, [dim1,dim2], order='C')
    return matrix.T

def readHorizon(dim,filename):
    with open(filename, 'rb') as f:    
        data = np.fromfile(filename, dtype=np.int32, count=dim)

    return data

nx = 1809
nt = 501
dx = 12.5
dt = 0.004
two_seconds = 375

hrz1 = np.array([readHorizon(1810,"hrzs/xhrz0_1810ams.bin"),readHorizon(1810,"hrzs/zhrz0.bin")])
hrz2 = np.array([readHorizon(1810,"hrzs/xhrz1_1810ams.bin"),readHorizon(1810,"hrzs/zhrz1.bin")])
hrz3 = np.array([readHorizon(1810,"hrzs/xhrz2_1810ams.bin"),readHorizon(1810,"hrzs/zhrz2.bin")])
hrz4 = np.array([readHorizon(1482,"hrzs/xhrz3_1482ams.bin"),readHorizon(1482,"hrzs/zhrz3.bin")])
hrz5 = np.array([readHorizon(1568,"hrzs/xhrz4_1568ams.bin"),readHorizon(1568,"hrzs/zhrz4.bin")])
hrz6 = np.array([readHorizon(1810,"hrzs/xhrz5_1810ams.bin"),readHorizon(1810,"hrzs/zhrz5.bin")])
hrz7 = np.array([readHorizon(1392,"hrzs/xhrz6_1392ams.bin"),readHorizon(1392,"hrzs/zhrz6.bin")])
hrz8 = np.array([readHorizon(1810,"hrzs/xhrz7_1810ams.bin"),readHorizon(1810,"hrzs/zhrz7.bin")])

realSection = readbinaryfile(nx,nt,"sectionReal.bin")
realSection = realSection[0:two_seconds,:]

nts = 3000
dts = 0.0005

sintSection = readbinaryfile(nx,nts,"sintheticSection.bin")
# sintSection = readbinaryfile(nx,nts,"sintheticSectionGradientModel.bin")

perc = np.percentile(realSection,[.5, 97.0])
realSectionPerc = exposure.rescale_intensity(realSection,in_range=(perc[0],perc[1]),out_range=(0,255))

t = np.arange(nts) * dts

for j in range(nx):
    sintSection[:,j] *= t**2 

perc = np.percentile(sintSection,[.5, 98.5])
sintSectionPerc = exposure.rescale_intensity(sintSection,in_range=(perc[0],perc[1]),out_range=(0,255))

locks_x = np.linspace(0,nx,7)
labels_x = np.round(np.linspace(8012.5,nx*dx+8012.5,7),decimals=1)

locks_t = np.linspace(0,two_seconds,5)
labels_t = np.around(locks_t * dt,decimals=1)

tloc = np.linspace(0,nts,5)
tlab = np.around(tloc * dts,decimals=1)

plt.figure(1,figsize=(15,5),dpi=200)

# plt.subplot(211)
# plt.imshow(realSectionPerc,cmap="Greys",aspect="auto")
# plt.title("Seção empilhada real",fontsize=20)
# plt.ylabel("Tempo [s]",fontsize=15)

# plt.scatter(hrz1[0],hrz1[1],marker=".")
# plt.scatter(hrz2[0],hrz2[1],marker=".")
# plt.scatter(hrz3[0],hrz3[1],marker=".")
# plt.scatter(hrz4[0],hrz4[1],marker=".")
# plt.scatter(hrz5[0],hrz5[1],marker=".")
# plt.scatter(hrz6[0],hrz6[1],marker=".")
# plt.scatter(hrz7[0],hrz7[1],marker=".")
# plt.scatter(hrz8[0],hrz8[1],marker=".",c="lightblue")

# plt.xticks(locks_x,labels_x)
# plt.yticks(locks_t,labels_t)
# plt.xlim([0,nx])

# plt.subplot(212)
plt.imshow(sintSectionPerc,cmap="Greys",aspect="auto")
# plt.title("Seção empilhada sintética",fontsize=20)
# plt.ylabel("Tempo [s]",fontsize=15)
# plt.xlabel("Distância [m]",fontsize=15)

# plt.scatter(hrz1[0],hrz1[1]*8,marker=".")
# plt.scatter(hrz2[0],hrz2[1]*8,marker=".")
# plt.scatter(hrz3[0],hrz3[1]*8,marker=".")
# plt.scatter(hrz4[0],hrz4[1]*8,marker=".")
# plt.scatter(hrz5[0],hrz5[1]*8,marker=".")
# plt.scatter(hrz6[0],hrz6[1]*8,marker=".")
# plt.scatter(hrz7[0],hrz7[1]*8,marker=".")
# plt.scatter(hrz8[0],hrz8[1]*8,marker=".",c="lightblue")

# plt.xticks(locks_x,labels_x)
# plt.yticks(tloc,tlab)
plt.xticks([])
plt.yticks([])

plt.xlim([0,nx])

plt.savefig("sectionLower.png",dpi=200,bbox_inches = "tight")
plt.tight_layout()
plt.show()
