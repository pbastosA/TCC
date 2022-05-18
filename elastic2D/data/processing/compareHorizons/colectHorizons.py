import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

from skimage import exposure

def readbinaryfile(dim1,dim2,filename):
    with open(filename, 'rb') as f:    
        data   = np.fromfile(filename, dtype= np.float32, count= dim1*dim2)
        matrix = np.reshape(data, [dim1,dim2], order='C')
    return matrix.T

def extractHorizons(N):
    zhrz1 = []
    xhrz1 = []

    for j in range(len(N[0])):
        for i in range(1,len(N)):
            if N[i,j] < 1.0:
                xhrz1.append(j) 
                zhrz1.append(i)    
            
    remove = []        
    for i in range(1,len(zhrz1)):
        if zhrz1[i] == zhrz1[i-1] + 1:
            remove.append(i)

    for i in range(len(remove)):
        xhrz1.pop(remove[i] - i)
        zhrz1.pop(remove[i] - i)

    return zhrz1, xhrz1

def readHorizon(dim,filename):
    with open(filename, 'rb') as f:    
        data = np.fromfile(filename, dtype=np.int32, count=dim)

    return data

def perc(matrix,value):
    p = np.percentile(matrix,[.5, value])                     
    image = exposure.rescale_intensity(matrix,                
                         in_range=(p[0],p[1]),                 
                         out_range=(0,255))                    
    return image                             

def geometricalSpreadCorrection(section,dt):

    t = np.arange(len(section)) * dt

    for i in range(len(section[0])):
        section[:,i] *= t**2

    return section

nx = 1809
nt = 501
dx = 12.5
dtr = 0.004
two_seconds = 375

realSection = readbinaryfile(nx,nt,"sectionReal.bin")
realSection = realSection[0:two_seconds,:]

nts = 3000
dts = 0.0005

sintSectionLow = readbinaryfile(nx,nts,"sintheticSection.bin")
sintSectionHig = readbinaryfile(nx,nts,"sintheticSectionGradientModel.bin")

# realSection = geometricalSpreadCorrection(realSection,dtr)
sintSectionLow = geometricalSpreadCorrection(sintSectionLow,dts)
sintSectionHig = geometricalSpreadCorrection(sintSectionHig,dts)

realSectionPerc = perc(realSection,97)
sintSectionLowPerc = perc(sintSectionLow,99)
sintSectionHigPerc = perc(sintSectionHig,99)

#%%
imgl = mpimg.imread("horizonLow.png")
imgh = mpimg.imread("horizonGrad.png")

Nl = imgl[:,:,0].copy()
Nh = imgh[:,:,0].copy()

nx = len(Nl[0])
nt = len(Nl)

h0l = []; x0l = []
h1l = []; x1l = []
h2l = []; x2l = []
h3l = []; x3l = []
h4l = []; x4l = []
h5l = []; x5l = []
h6l = []; x6l = []
h7l = []; x7l = []

h0h = []; x0h = []
h1h = []; x1h = []
h2h = []; x2h = []
h3h = []; x3h = []
h4h = []; x4h = []
h5h = []; x5h = []
h6h = []; x6h = []
h7h = []; x7h = []

hrz1 = np.array([readHorizon(1810,"../hrzs/xhrz0_1810ams.bin"),readHorizon(1810,"../hrzs/zhrz0.bin")])
hrz2 = np.array([readHorizon(1810,"../hrzs/xhrz1_1810ams.bin"),readHorizon(1810,"../hrzs/zhrz1.bin")])
hrz3 = np.array([readHorizon(1810,"../hrzs/xhrz2_1810ams.bin"),readHorizon(1810,"../hrzs/zhrz2.bin")])
hrz4 = np.array([readHorizon(1482,"../hrzs/xhrz3_1482ams.bin"),readHorizon(1482,"../hrzs/zhrz3.bin")])
hrz5 = np.array([readHorizon(1568,"../hrzs/xhrz4_1568ams.bin"),readHorizon(1568,"../hrzs/zhrz4.bin")])
hrz6 = np.array([readHorizon(1810,"../hrzs/xhrz5_1810ams.bin"),readHorizon(1810,"../hrzs/zhrz5.bin")])
hrz7 = np.array([readHorizon(1392,"../hrzs/xhrz6_1392ams.bin"),readHorizon(1392,"../hrzs/zhrz6.bin")])
hrz8 = np.array([readHorizon(1810,"../hrzs/xhrz7_1810ams.bin"),readHorizon(1810,"../hrzs/zhrz7.bin")])

zhrz1, xhrz1 = extractHorizons(Nl)
zhrz2, xhrz2 = extractHorizons(Nh)

xhrz1 = np.array(xhrz1)
zhrz1 = np.array(zhrz1)

xhrz2 = np.array(xhrz2)
zhrz2 = np.array(zhrz2)

x = np.arange(len(Nl[0]))

for i in range(len(x)):
    layers1 = np.where(xhrz1 == i)[0]
    layers2 = np.where(xhrz2 == i)[0]

    h0l.append(zhrz1[layers1[0]]); x0l.append(i)
    h1l.append(zhrz1[layers1[1]]); x1l.append(i)
    h2l.append(zhrz1[layers1[2]]); x2l.append(i)

    h0h.append(zhrz2[layers2[0]]); x0h.append(i)
    h1h.append(zhrz2[layers2[1]]); x1h.append(i)
    h2h.append(zhrz2[layers2[2]]); x2h.append(i)

    if i <= 1474:
        h5l.append(zhrz1[layers1[5]]); x5l.append(i)

    if i <= 1480:
        # h3l.append(zhrz1[layers[3]]); x3l.append(i)
        # h4l.append(zhrz1[layers[4]]); x4l.append(i)
        h5h.append(zhrz2[layers2[5]]); x5h.append(i)
    
    if 1474 < i <= 1564:
        h5l.append(zhrz1[layers1[4]]); x5l.append(i)  

    if 1480 < i <= 1563:
        # h4l.append(zhrz1[layers[3]]); x4l.append(i)  
        h5h.append(zhrz2[layers2[4]]); x5h.append(i)  
        
    if i > 1564:
        h5l.append(zhrz1[layers1[3]]); x5l.append(i)  
        
    if i > 1563:
        h5h.append(zhrz2[layers2[3]]); x5h.append(i)  

    # if 105 <= i <= 1327: 

    # if 99 <= i <= 1317: 
    #     h6l.append(zhrz1[layers[6]]); x6l.append(i) 
    
    # # if 1414 <= i <= 1474:
    # if 1410 <= i <= 1484:
    #     h6l.append(zhrz1[layers[6]]); x6l.append(i) 
    
    # # if 1474 < i <= 1548:
    # if 1480 < i <= 1576:
    #     h6l.append(zhrz1[layers[5]]); x6l.append(i) 

    h7l.append(zhrz1[layers1[-1]]); x7l.append(i)
    h7h.append(zhrz2[layers2[-1]]); x7h.append(i)

#%%
dt = 0.004
time = np.arange(nt) * dt

ndiffs = 5

diffLow = np.zeros((nx,ndiffs))
diffHig = np.zeros((nx,ndiffs))

diffLow[:,0] = np.array(np.abs(hrz1[1] - h0l),dtype=int)
diffLow[:,1] = np.array(np.abs(hrz2[1] - h1l),dtype=int)
diffLow[:,2] = np.array(np.abs(hrz3[1] - h2l),dtype=int)
diffLow[:,3] = np.array(np.abs(hrz6[1] - h5l),dtype=int)
diffLow[:,4] = np.array(np.abs(hrz8[1] - h7l),dtype=int)

diffHig[:,0] = np.array(np.abs(hrz1[1] - h0h),dtype=int)-1
diffHig[:,1] = np.array(np.abs(hrz2[1] - h1h),dtype=int)
diffHig[:,2] = np.array(np.abs(hrz3[1] - h2h),dtype=int)
diffHig[:,3] = np.array(np.abs(hrz6[1] - h5h),dtype=int)
diffHig[:,4] = np.array(np.abs(hrz8[1] - h7h),dtype=int)

espectLow = np.zeros((nt,5))
espectHig = np.zeros((nt,5))

for i in range(nt):
    for j in range(ndiffs):
        espectLow[i,j] += len(np.where(i == diffLow[:,j])[0])
        espectHig[i,j] += len(np.where(i == diffHig[:,j])[0])

for i in range(ndiffs):
    espectLow[:,i] *= 1.0 / np.max(espectLow[:,i]) 
    espectHig[:,i] *= 1.0 / np.max(espectHig[:,i]) 

#%%

plt.figure(1,figsize=(10,10))

plt.subplot(151)
plt.plot(espectLow[:,0],time)
plt.plot(espectHig[:,0],time)
plt.ylim([0,0.3])
plt.gca().invert_yaxis()
plt.title("$e_{abs}$(hrz0)")
plt.legend(["Bruto","Corrig."],loc="lower left")
plt.ylabel("Tempo [s]",fontsize=12)
plt.xlabel("Amplitude",fontsize=12)

plt.subplot(152)
plt.plot(espectLow[:,1],time)
plt.plot(espectHig[:,1],time)
plt.ylim([0,0.3])
plt.gca().set_yticklabels([])
plt.gca().invert_yaxis()
plt.title("$e_{abs}$(hrz1)")
plt.legend(["Bruto","Corrig."],loc="lower left")
plt.xlabel("Amplitude",fontsize=12)

plt.subplot(153)
plt.plot(espectLow[:,2],time)
plt.plot(espectHig[:,2],time)
plt.ylim([0,0.3])
plt.gca().set_yticklabels([])
plt.gca().invert_yaxis()
plt.title("$e_{abs}$(hrz2)")
plt.legend(["Bruto","Corrig."],loc="lower left")
plt.xlabel("Amplitude",fontsize=12)

plt.subplot(154)
plt.plot(espectLow[:,3],time)
plt.plot(espectHig[:,3],time)
plt.ylim([0,0.3])
plt.gca().set_yticklabels([])
plt.gca().invert_yaxis()
plt.title("$e_{abs}$(hrz5)")
plt.legend(["Bruto","Corrig."],loc="lower left")
plt.xlabel("Amplitude",fontsize=12)

plt.subplot(155)
plt.plot(espectLow[:,4],time)
plt.plot(espectHig[:,4],time)
plt.ylim([0,0.3])
plt.gca().set_yticklabels([])
plt.gca().invert_yaxis()
plt.title("$e_{abs}$(hrz7)")
plt.legend(["Bruto","Corrig."],loc="lower left")
plt.xlabel("Amplitude",fontsize=12)

plt.tight_layout()
plt.savefig("analise.png",dpi=200,bbox_inches="tight")

#%%

nx = 1809

locks_x = np.linspace(0,nx,7)
labels_x = np.round(np.linspace(8012.5,nx*dx+8012.5,7),decimals=1)

locks_t = np.linspace(0,two_seconds,5)
labels_t = np.around(locks_t * dtr,decimals=1)

tloc = np.linspace(0,nts,5)
tlab = np.around(tloc * dts,decimals=1)

plt.figure(2,figsize=(15,14))

plt.subplot(311)
plt.imshow(realSectionPerc,aspect="auto",cmap="Greys")
plt.scatter(hrz1[0],hrz1[1],marker=".")
plt.scatter(hrz2[0],hrz2[1],marker=".")
plt.scatter(hrz3[0],hrz3[1],marker=".")
plt.scatter(hrz6[0],hrz6[1],marker=".")
plt.scatter(hrz8[0],hrz8[1],marker=".",c="lightblue")
plt.legend(["hrz0","hrz1","hrz2","hrz5","hrz7"],loc="lower right",fontsize=14)

plt.ylabel("Tempo [s]",fontsize=15)
plt.title("Seção empilhada real",fontsize=20)

plt.xticks(locks_x,labels_x)
plt.yticks(locks_t,labels_t)

plt.ylim([0,nt])
plt.xlim([0,nx])
plt.gca().invert_yaxis()

plt.subplot(312)
plt.imshow(sintSectionLowPerc,aspect="auto",cmap="Greys")
plt.scatter(x0l,np.array(h0l)*8,marker=".")
plt.scatter(x1l,np.array(h1l)*8,marker=".")
plt.scatter(x2l,np.array(h2l)*8,marker=".")
plt.scatter(x5l,np.array(h5l)*8,marker=".")
plt.scatter(x7l,np.array(h7l)*8,marker=".",c="lightblue")
plt.legend(["hrz0","hrz1","hrz2","hrz5","hrz7"],loc="lower right",fontsize=14)

plt.ylabel("Tempo [s]",fontsize=15)
plt.title("Seção empilhada sintética - modelo bruto",fontsize=20)

plt.xticks(locks_x,labels_x)
plt.yticks(tloc,tlab)

plt.ylim([0,nt*8])
plt.xlim([0,nx])
plt.gca().invert_yaxis()

plt.subplot(313)
plt.imshow(sintSectionHigPerc,aspect="auto",cmap="Greys")
plt.scatter(x0h,np.array(h0h)*8,marker=".")
plt.scatter(x1h,np.array(h1h)*8,marker=".")
plt.scatter(x2h,np.array(h2h)*8,marker=".")
plt.scatter(x5h,np.array(h5h)*8,marker=".")
plt.scatter(x7h,np.array(h7h)*8,marker=".",c="lightblue")
plt.legend(["hrz0","hrz1","hrz2","hrz5","hrz7"],loc="lower right",fontsize=14)

plt.ylabel("Tempo [s]",fontsize=15)
plt.xlabel("Distância [m]",fontsize=15)
plt.title("Seção empilhada sintética - modelo corrigido",fontsize=20)

plt.xticks(locks_x,labels_x)
plt.yticks(tloc,tlab)

plt.ylim([0,nt*8])
plt.xlim([0,nx])
plt.gca().invert_yaxis()

plt.tight_layout()
plt.savefig("interpHrz.png",dpi=200,bbox_inches="tight")

plt.show()






