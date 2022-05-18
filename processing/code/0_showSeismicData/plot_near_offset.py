import numpy as np
from skimage import exposure
import matplotlib.pyplot as plt

def readbinaryfile(dim1,dim2,filename):
    with open(filename, 'rb') as f:    
        data   = np.fromfile(filename, dtype= np.float32, count= dim1*dim2)
        matrix = np.reshape(data, [dim1,dim2], order='C')
    return matrix.T

dt = 0.004
traces = 2128
samples = 2301

t = np.array([0,0,0.2,0.4,0.6,0.8,1.0,1.2,1.4,1.6])

nearOffset = readbinaryfile(traces,samples,"CMP10123/data_offset_10850.bin")
nearOffset_old = nearOffset[0:400,:]

perc = np.percentile(nearOffset_old,[.5, 99.0])
nearOffset_old = exposure.rescale_intensity(nearOffset_old,in_range=(perc[0],perc[1]),out_range=(0,255))

plt.figure(figsize=(10,5),dpi=150)

cbar = plt.colorbar(plt.imshow(nearOffset,aspect="auto",cmap="Greys"),fraction=0.025)
cbar.set_label("Amplitude",fontsize = 15, rotation = 90)

plt.imshow(nearOffset_old,aspect="auto",cmap="Greys")
plt.title("Offset 10850 - near offset PREMIG")
plt.xlabel("Traços")
plt.ylabel("Tempo [s]")
plt.subplot().set_yticklabels(t)

plt.savefig("nearOffset.png",dpi=200,bbox_inches="tight")
plt.show()
