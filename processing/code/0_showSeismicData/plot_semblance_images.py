import numpy as np
import matplotlib.pyplot as plt

def readbinaryfile(dim1,dim2,filename):
    with open(filename, 'rb') as f:    
        data   = np.fromfile(filename, dtype= np.float32, count= dim1*dim2)
        matrix = np.reshape(data, [dim1,dim2], order='C')
    return matrix.T

veloc = 150
tempo = 461

t = np.linspace(0,9,461)       # todos os tempos da discretização adequada
v = np.linspace(1500,6000,150) # todas as velocidades com discretização adequada

t = np.array([0.00,0.00,1.95,3.91,5.86,7.82])
v = np.array([0, 1500, 3010, 4520])

raw_semblance_9945 = readbinaryfile(veloc,tempo,"CMP10123/semblance_CMP_raw_9945.bin")
raw_semblance_11263 = readbinaryfile(veloc,tempo,"CMP10123/semblance_CMP_raw_11263.bin")
raw_semblance_13543 = readbinaryfile(veloc,tempo,"CMP10123/semblance_CMP_raw_13543.bin")

cont = 0
images = np.array([raw_semblance_9945,raw_semblance_11263,raw_semblance_13543])

fig, axes = plt.subplots(ncols=3,nrows=1,dpi=150)
fig.set_size_inches(10,8)

axes[0].set_title("Semblance - CMP 9945")
axes[0].set_ylabel("Tempos [s]",fontsize=15)
axes[0].set_xlabel("Velocidades [m/s]",fontsize=15)
axes[0].set_yticklabels(t)    
axes[0].set_xticklabels(v)

axes[1].set_title("Semblance - CMP 11263")
axes[1].set_yticklabels([])
axes[1].set_xlabel("Velocidades [m/s]",fontsize=15)
axes[1].set_xticklabels(v)

axes[2].set_title("Semblance - CMP 13543")
axes[2].set_yticklabels([])
axes[2].set_xlabel("Velocidades [m/s]",fontsize=15)
axes[2].set_xticklabels(v)

for ax in axes.flat:
    im = ax.imshow(images[cont],aspect="auto",cmap="Greys")
    cont += 1

cbar = fig.colorbar(im,aspect="auto",cmap="Greys",ax=axes.flat,fraction=0.025)
cbar.set_label("Correlação",fontsize = 15, rotation = 90)

plt.savefig("semblance_CMPs.png",dpi=200,bbox_inches='tight')
plt.show()