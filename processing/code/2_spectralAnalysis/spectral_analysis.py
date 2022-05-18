#%% Bibliotecas utilizadas
import sys
import numpy as np
from skimage import exposure
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

#%% Funções utilizadas 

def readbinaryfile(dim1,dim2,filename):
    with open(filename, 'rb') as f:    
        data   = np.fromfile(filename, dtype= np.float32, count= dim1*dim2)
        matrix = np.reshape(data, [dim1,dim2], order='C')
    return matrix.T

#%% Declarando variáveis

nt = 2301
nx = 1064
dt = 0.004
stopTime = 500
j = complex(0,1)

#%% Lendo o arquivo cdp ajustando a escala de cor

offset_raw = readbinaryfile(nx,nt,"nearOffset.bin")

perc = np.percentile(offset_raw,[.5, 99.0])
offset = exposure.rescale_intensity(offset_raw,in_range=(perc[0],perc[1]),out_range=(0,255))

#%% Plotado o cdp completo

locks_t = np.linspace(0,stopTime,11)
labels_t = [0.0,0.2,0.4,0.6,0.8,1.0,1.2,1.4,1.6,1.8,2.0]

rect = Rectangle((298,0),3,500,linewidth=1,edgecolor='r',facecolor='none')

# plt.figure(1,figsize=(15,5))
# cbar = plt.colorbar(plt.imshow(offset_raw[0:stopTime,:],cmap="Greys",aspect="auto"))
# cbar.set_label("Amplitudes")
# plt.imshow(offset[0:stopTime,:],cmap="Greys",aspect="auto")
# plt.title("Near offset gather",fontsize=15)
# plt.xlabel("Traços",fontsize=15)
# plt.ylabel("Tempo [s]",fontsize=15)
# plt.yticks(locks_t,labels_t)
# plt.gca().add_patch(rect)
# plt.legend(["Traço selecionado"])
# plt.savefig("nearOffset_marked.png",bbox_inches="tight",dpi=200)


#%% Retirando um traço do offset

trace = offset_raw[0:stopTime,300]
times = np.arange(stopTime)   

#%% Plotando o traço
# rect1 = Rectangle((-5000,37),18000,10,linewidth=1,edgecolor='r',facecolor='none')
# rect2 = Rectangle((-5000,51),18000,10,linewidth=1,edgecolor='b',facecolor='none')
# rect3 = Rectangle((-5000,143),18000,10,linewidth=1,edgecolor='k',facecolor='none')
# rect4 = Rectangle((-5000,417),18000,10,linewidth=1,edgecolor='m',facecolor='none')

# plt.figure(2,figsize=(6,10))
# plt.plot(trace,times)
# plt.title("Traço escolhido para a análise",fontsize=15)
# plt.xlabel("Amplitude",fontsize=15)
# plt.ylabel("Tempo [s]",fontsize=15)
# plt.gca().add_patch(rect1)
# plt.gca().add_patch(rect2)
# plt.gca().add_patch(rect3)
# plt.gca().add_patch(rect4)
# plt.yticks(locks_t,labels_t)
# plt.gca().invert_yaxis()
# plt.legend(["Near Offset do tiro 300","Pulso fundo do mar","Segundo pulso","Terceiro pulso","Quarto pulso"])
# plt.savefig("trace300_marked.png",bbox_inches="tight",dpi=200)

#%% Isolando tres pulsos para analise espectral 

ams_min = np.array([37,51,143,417])
ams_max = np.array([47,61,153,427])

window1 = np.zeros(len(trace))  # Fundo do mar
window2 = np.zeros(len(trace))  # Camada 1
window3 = np.zeros(len(trace))  # Camada 2
window4 = np.zeros(len(trace))  # camada 3

window1[ams_min[0]:ams_max[0]] = trace[ams_min[0]:ams_max[0]]
window2[ams_min[1]:ams_max[1]] = trace[ams_min[1]:ams_max[1]]
window3[ams_min[2]:ams_max[2]] = trace[ams_min[2]:ams_max[2]]
window4[ams_min[3]:ams_max[3]] = trace[ams_min[3]:ams_max[3]]

#%% Plotando pulso do fundo do mar

# plt.figure(3,figsize=(6,10))
# plt.plot(window1,times)
# plt.title("Pulso do fundo marinho",fontsize=15)
# plt.xlabel("Amplitude",fontsize=15)
# plt.ylabel("Tempo [s]",fontsize=15)
# plt.yticks(locks_t,labels_t)
# plt.ylim([0,100])
# plt.gca().invert_yaxis()
# plt.savefig("fundoMar.png",dpi=200,bbox_inches="tight")

# plt.figure(4,figsize=(6,10))
# plt.plot(window2,times)
# plt.title("Segundo pulso",fontsize=15)
# plt.xlabel("Amplitude",fontsize=15)
# plt.yticks(locks_t,labels_t)
# plt.ylim([0,100])
# plt.gca().invert_yaxis()
# plt.savefig("pulso2.png",dpi=200,bbox_inches="tight")

# plt.figure(5,figsize=(6,10))
# plt.plot(window3,times)
# plt.title("Terceiro pulso",fontsize=15)
# plt.xlabel("Amplitude",fontsize=15)
# plt.yticks(locks_t,labels_t)
# plt.ylim([100,200])
# plt.gca().invert_yaxis()
# plt.savefig("pulso3.png",dpi=200,bbox_inches="tight")

# plt.figure(6,figsize=(6,10))
# plt.plot(window4,times)
# plt.title("Quarto pulso",fontsize=15)
# plt.xlabel("Amplitude",fontsize=15)
# plt.yticks(locks_t,labels_t)
# plt.ylim([375,475])
# plt.gca().invert_yaxis()
# plt.savefig("pulso4.png",dpi=200,bbox_inches="tight")

#%% Transformada de Fourier dos pulsos

freqs = np.fft.fftfreq(stopTime,dt) # frequências iguais para todos os pulsos

fwindow1 = np.fft.fft(window1)
fwindow2 = np.fft.fft(window2)
fwindow3 = np.fft.fft(window3)
fwindow4 = np.fft.fft(window4)

# plt.figure(7,figsize=(6,10))
# plt.plot(np.abs(fwindow1),freqs)
# plt.title("Espectro do fundo marinho",fontsize=15)
# plt.xlabel("Amplitude",fontsize=15)
# plt.ylabel("Frequências [Hz]",fontsize=15)
# plt.ylim([0,125])
# plt.gca().invert_yaxis()
# plt.grid()
# plt.savefig("espAmpFundoMar.png",dpi=200,bbox_inches="tight")

# plt.figure(8,figsize=(6,10))
# plt.plot(np.abs(fwindow2),freqs)
# plt.title("Espectro do segundo pulso",fontsize=15)
# plt.xlabel("Amplitude",fontsize=15)
# plt.ylim([0,125])
# plt.gca().invert_yaxis()
# plt.grid()
# plt.savefig("espAmpPulso2.png",dpi=200,bbox_inches="tight")

# plt.figure(9,figsize=(6,10))
# plt.plot(np.abs(fwindow3),freqs)
# plt.title("Espectro do terceiro pulso",fontsize=15)
# plt.xlabel("Amplitude",fontsize=15)
# plt.ylim([0,125])
# plt.gca().invert_yaxis()
# plt.grid()
# plt.savefig("espAmpPulso3.png",dpi=200,bbox_inches="tight")

# plt.figure(10,figsize=(6,10))
# plt.plot(np.abs(fwindow4),freqs)
# plt.title("Espectro do quarto pulso",fontsize=15)
# plt.xlabel("Amplitude",fontsize=15)
# plt.ylim([0,125])
# plt.gca().invert_yaxis()
# plt.grid()
# plt.savefig("espAmpPulso4.png",dpi=200,bbox_inches="tight")

#%% Espectro de fase dos pulsos isolados

angle1 = np.angle(fwindow1) * 180/np.pi
angle2 = np.angle(fwindow2) * 180/np.pi
angle3 = np.angle(fwindow3) * 180/np.pi
angle4 = np.angle(fwindow4) * 180/np.pi

plt.figure(11,figsize=(6,10))
plt.plot(angle1,freqs,"*")
plt.title("Espectro do fundo marinho",fontsize=15)
plt.xlabel("Fase [°]",fontsize=15)
plt.ylabel("Frequências [Hz]",fontsize=15)
plt.ylim([30,40])
plt.gca().invert_yaxis()
plt.grid()
plt.savefig("espFaseFundoMar.png",dpi=200,bbox_inches="tight")

plt.figure(12,figsize=(6,10))
plt.plot(angle2,freqs,"*")
plt.title("Espectro do segundo pulso",fontsize=15)
plt.xlabel("Fase [°]",fontsize=15)
plt.ylim([30,40])
plt.gca().invert_yaxis()
plt.grid()
plt.savefig("espFasePulso2.png",dpi=200,bbox_inches="tight")

plt.figure(13,figsize=(6,10))
plt.plot(angle3,freqs,"-")
plt.title("Espectro do terceiro pulso",fontsize=15)
plt.xlabel("Fase [°]",fontsize=15)
plt.ylim([30,40])
plt.gca().invert_yaxis()
plt.grid()
plt.savefig("espFasePulso3.png",dpi=200,bbox_inches="tight")

plt.figure(14,figsize=(6,10))
plt.plot(angle4,freqs,"*")
plt.title("Espectro do pulso 4",fontsize=15)
plt.xlabel("Fase [°]",fontsize=15)
plt.ylim([30,40])
plt.gca().invert_yaxis()
plt.grid()
plt.savefig("espFasePulso4.png",dpi=200,bbox_inches="tight")

plt.show()