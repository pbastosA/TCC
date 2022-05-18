import sys
from skimage import exposure
import numpy as np
import matplotlib.pyplot as plt

def readbinaryfile(dim1,dim2,filename):
    with open(filename, 'rb') as f:    
        data   = np.fromfile(filename, dtype= np.float32, count= dim1*dim2)
        matrix = np.reshape(data, [dim1,dim2], order='C')
    return matrix.T

dt = 0.004
spread = 160
nt = 2301
t = np.array([0, 0, 500, 1000, 1500, 2000]) * dt

flt_cdp_init = readbinaryfile(spread,nt,"CMP10123/cdp_flt_10123.bin")
raw_cdp_init = readbinaryfile(spread,nt,"CMP10123/cdp_raw_10123.bin")
mig_cdp_init = readbinaryfile(spread,nt,"CMP10123/cdp_mig_10123.bin")

perc1 = np.percentile(flt_cdp_init,[.5, 99.0])
perc2 = np.percentile(raw_cdp_init,[.5, 99.0])
perc3 = np.percentile(mig_cdp_init,[.5, 99.0])

flt_cdp = exposure.rescale_intensity(flt_cdp_init,in_range=(perc1[0],perc1[1]),out_range=(0,255))
raw_cdp = exposure.rescale_intensity(raw_cdp_init,in_range=(perc2[0],perc2[1]),out_range=(0,255))
mig_cdp = exposure.rescale_intensity(mig_cdp_init,in_range=(perc3[0],perc3[1]),out_range=(0,255))

cont = 0
images = np.array([flt_cdp,raw_cdp,mig_cdp])

fig, axes = plt.subplots(ncols=3,nrows=1,dpi=150)
fig.set_size_inches(10,8)

axes[0].imshow(flt_cdp_init,aspect="auto",cmap="Greys")
axes[0].set_title("CMP 10123 - MGFLT")
axes[0].set_ylabel("Tempo [s]",fontsize=15)
axes[0].set_xlabel("Traços",fontsize=15)
axes[0].set_yticklabels(t)    

axes[1].imshow(raw_cdp_init,aspect="auto",cmap="Greys")
axes[1].set_title("CMP 10123 - MGRAW")
axes[1].set_yticklabels([])
axes[1].set_xlabel("Traços",fontsize=15)

axes[2].imshow(mig_cdp_init,aspect="auto",cmap="Greys")
axes[2].set_title("CMP 10123 - PREMIG")
axes[2].set_yticklabels([])
axes[2].set_xlabel("Traços",fontsize=15)

cbar = fig.colorbar(axes[0].imshow(flt_cdp_init,aspect="auto",cmap="Greys"),ax=axes.flat,fraction=0.025)
cbar.set_label("Amplitude",fontsize = 15, rotation = 90)

for ax in axes.flat:
    im = ax.imshow(images[cont],aspect="auto",cmap="Greys")
    cont += 1

plt.savefig("seismograms.png",dpi=200,bbox_inches='tight')
plt.show()