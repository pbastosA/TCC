import sys
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

from skimage import exposure 

def readbinaryfile(dim1,dim2,filename):
    with open(filename, 'rb') as f:    
        data   = np.fromfile(filename, dtype= np.float32, count= dim1*dim2)
        matrix = np.reshape(data, [dim1,dim2], order='F')
    return matrix

def perc(matrix,value):
    p = np.percentile(matrix,[.5, value])
    image = exposure.rescale_intensity(matrix,in_range=(p[0],p[1]),out_range=(0,255))    

    return image 

nx = 5644
nz = 425
dx = 6.250
dz = 6.514

nabc = 50
nsnaps = 30

snapVp  = np.zeros((nz,nx,nsnaps))
snapVs  = np.zeros((nz,nx,nsnaps))
snapRho = np.zeros((nz,nx,nsnaps))

for i in range(nsnaps):
    snapVp[:,:,i]  = readbinaryfile(nx,nz,f"snaps/snapVp{i*100}.bin").T
    snapVs[:,:,i]  = readbinaryfile(nx,nz,f"snaps/snapVs{i*100}.bin").T
    snapRho[:,:,i] = readbinaryfile(nx,nz,f"snaps/snapRho{i*100}.bin").T

snapVp = snapVp[nabc:nz-nabc,nabc:nx-nabc,:]
snapVs = snapVs[nabc:nz-nabc,nabc:nx-nabc,:]
snapRho = snapRho[nabc:nz-nabc,nabc:nx-nabc,:]

nx = 5544
nz = 325

# plt.figure(3,figsize=(15,10))
# plt.subplot(311)
# plt.imshow(perc(snapVp[:,:,10],99.5),aspect="auto",cmap="Greys")

# plt.subplot(312)
# plt.imshow(perc(snapVs[:,:,10],99.5),aspect="auto",cmap="Greys")

# plt.subplot(313)
# plt.imshow(perc(snapRho[:,:,10],99.5),aspect="auto",cmap="Greys")

fig, ax = plt.subplots(nrows = 3, ncols = 1, figsize = (15,12), dpi = 200)

xloc = np.linspace(0,nx,11,dtype=int)
xlab = np.linspace(0,nx*dx,11,dtype=int)

zloc = np.linspace(0,nz,5)
zlab = np.linspace(0,nz*dz,5,dtype=int)

ims = []
for i in range(0,nsnaps):
   
    im1 = ax[0].imshow(perc(snapVp[:,:,i],99.5), animated=True,aspect="auto",cmap="Greys")
    im2 = ax[1].imshow(perc(snapVs[:,:,i],99.5), animated=True,aspect="auto",cmap="Greys")
    im3 = ax[2].imshow(perc(snapRho[:,:,i],99.5), animated=True,aspect="auto",cmap="Greys")

    if i == 0:
        ax[0].imshow(perc(snapVp[:,:,i],99.5),aspect="auto",cmap="Greys")  # show an initial one first
        ax[1].imshow(perc(snapVs[:,:,i],99.5),aspect="auto",cmap="Greys")  # show an initial one first
        ax[2].imshow(perc(snapRho[:,:,i],99.5),aspect="auto",cmap="Greys")  # show an initial one first
    
    ims.append([im1,im2,im3])

ani = animation.ArtistAnimation(fig, ims, interval=500, blit=True, repeat_delay=500)

ax[0].set_title("Snapshot projetado em Vp",fontsize=15)
ax[1].set_title("Snapshot projetado em Vs",fontsize=15)
ax[2].set_title("Snapshot projetado na Densidade",fontsize=15)

ax[0].set_ylabel("Profundidade [m]",fontsize=15)
ax[1].set_ylabel("Profundidade [m]",fontsize=15)
ax[2].set_ylabel("Profundidade [m]",fontsize=15)

ax[2].set_xlabel("Distância [m]",fontsize=15)

plt.setp(ax,xticks=xloc, xticklabels=xlab, yticks=zloc, yticklabels=zlab)

# plt.tight_layout()
# plt.show()

Writer = animation.writers['pillow']

writer = Writer(fps=10, metadata=dict(artist='Paulo'), bitrate=100)
ani.save('snapshots.gif',writer=writer)

