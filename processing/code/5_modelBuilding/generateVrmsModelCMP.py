#%% Bibliotecas

import sys
import numpy as np
import matplotlib.pyplot as plt

#%% Funções usadas

def read_vpick_iva(filename,dt = None,timeStop = None):
    '''
    ----------------------------------------------------------------------
    Inputs:
    ----------------------------------------------------------------------    
    filename - path of the velocities picks outputed to iva.sh. 

    dt - if you waht to transform tnmo in samples, to construct a model. 

    timeStop - to truncate data at specified time, if do you want to see
               the times in seconds, just type the second parameter, if
               do you want to see time in samples, please especify dt 
               parameter. 
    
    ---------------------------------------------------------------------
    Outputs: [ in order ]
    ---------------------------------------------------------------------
        TNMO at each pick.

        VNMO at each pick.

        Picks index at each CMP (zero to nCMP analized).                
    '''

    # Read text file
    data = np.loadtxt(filename,skiprows=2,dtype=str,comments="\\")

    # Cleaning data, removing tnmo and vnmo names 
    for i in range(len(data)):
        data[i] = data[i][5:]

    tnmo = data[0::2]  # Times values in str format
    vnmo = data[1::2]  # Velocities values in str format

    timeSample = []    # Returned array with all times values in samples
    velocity = []      # Returned array with all valocities values
    coordPicks = []    # Returned array with all position of CMP analized (0 to nCMP)
    picksPerCMP = []   # Returned array with all picks per CMP 

    for i in range(len(tnmo)):
        
        t = " "  # It is a unit of time, it'll be transform in float value
        v = " "  # It is a unit of velocity

        auxTime = [] # All time values per CMP (all picks) 
        for j in tnmo[i]:
            if j == ',':    
                if dt == None:
                    auxTime.append(float(t)) # Convertion to float only 
                else:
                    auxTime.append(int(float(t) / dt)) # Convertion float to sample time
                
                t = " " 
            else:
                t += j

        auxVelocity= [] # All velocities values per CMP (all picks)
        for j in vnmo[i]:
            
            # Taking velocities values
            if j == ',':
                auxVelocity.append(float(v)) 
                v = " "
            else:
                v += j

        for j in range(len(auxTime)):
        
            if timeStop == None:
                timeSample.append(auxTime[j])
                velocity.append(auxVelocity[j])
            
            else:
                if auxTime[j] < timeStop: 
                    timeSample.append(auxTime[j])
                    velocity.append(auxVelocity[j])
                
    cont = 1
    for i in range(1,len(timeSample)):
        
        # Taking picks for the last CMP 
        if i == len(timeSample)-1: 
            picksPerCMP.append(cont+1)    
        
        # Comparing if change CMP picks     
        elif timeSample[i-1] < timeSample[i]:
            cont += 1   
        
        # Adding the picks per CMP at each CMP
        else:
            picksPerCMP.append(cont)
            cont = 1        
    
    cont = 0
    for i in picksPerCMP:
        
        # Catching the pich positions at each CMP
        coordPicks = np.append(coordPicks,np.ones(i) * cont)
        cont += 1 

    return timeSample, velocity, coordPicks, picksPerCMP   

def interp_irreg_1D(array):

    old = 0 # Lastest non zero value  
    i = 0   # None spaces 

    while True:
        # Counting zeros values 
        while array[old + i + 1] == 0.0:            
            i += 1

        # Parameter to interpolate
        parameter = (array[old + i + 1] - array[old]) / (i+1)
        
        # Interpolating array    
        for k in range(1,i+1):
            array[old + k] = array[old] + k*parameter 

        # Atualizing variables    
        old += i+1
        i = 0 

        # Stopping when reach the end of array
        if old + i + 1 >= len(array)-1:
            break

#%% Todas as variaveis usadas e seus respectivos significados

nt = 501                              # Tempo em amostras do modelo de velocidades RMS
dt = 0.004                            # Discretização temporal do dado sísmico
n = "../4_velocityAnalysis/vpick.txt" # Nome do arquivo de saída do iva.sh
 
nCDP = 11                             # Número de CMPs analizados no iva.sh
CMPs = np.zeros((nt,nCDP))            # Matriz dos pickings analizados por CMP

nx = 1810                             # Quantidade de CMPs completos na sísmica
esp = 180                             # Espaçamento entre os CMPs analizados 

modelo_RMS = np.zeros((nt,nx))        # Modelo de velocidades RMS completo 
modelo_INT = np.zeros((nt,nx))        # Modelo de velocidades Intervalares completo
cmp_positions = np.arange(0,nx,esp)   # Posição dos CMPs analizados em relação aos CMPs completos 

#%% Lendo o arquivo de saida do iva.sh

time,vel,coord,picks = read_vpick_iva(n,dt)
p1time,p1vel,p1coord,picks = read_vpick_iva(n)
p2time,p2vel,p2coord,picks = read_vpick_iva(n,timeStop=2)

# Mostrando os picks de maneira geral 
plt.figure(1,figsize=(15,5))
plt.scatter(p1coord,p1time,c = p1vel)
plt.ylim([0,2.0])
plt.gca().invert_yaxis()
cbar = plt.colorbar()
cbar.set_label("Velocidade RMS [m/s]",fontsize=15)
plt.title("Picks por CMP analisado",fontsize=20)
plt.xlabel("CMP analisado",fontsize=15)
plt.ylabel("Tempo [s]",fontsize=15)
plt.savefig("picksFocado.png",dpi=200,bbox_inches="tight")

#%% Agrupando os CMPs e interpolando traço a traço

# Coletando os pickings de velocidade 
for i in range(len(vel)):
    CMPs[int(time[i]),int(coord[i])] = vel[i] 

# Preenchendo os valores estimados para topo e base (necessários para a interpolação)
CMPs[0,:] = 1490
CMPs[-1,:] = 4000

# for k in range(len(picks)):
#     vint = np.zeros(picks[k])
#     vint[0] = vel[0+sum(picks[:k])]
#     for i in range(1,picks[k]):    
#         vint[i] = np.sqrt((vel[i+sum(picks[:k])]**2 * dt*time[i+sum(picks[:k])] - vel[i-1+sum(picks[:k])]**2 * dt*time[i-1+sum(picks[:k])]) / (dt*time[i+sum(picks[:k])] - dt*time[i-1+sum(picks[:k])]))

#         CMPs[int(time[i+sum(picks[:k])]),int(coord[i++sum(picks[:k])])] = vint[i]

#     for i in range(len(vint)):
#         print(f"{time[i+sum(picks[:k])]*dt:.3f} {vel[i+sum(picks[:k])]:.2f} {vint[i]:.2f}")

#     print("=-"*20)
#%% Interpolação 1D irregular traço a traço

for col in range(len(CMPs[0,:])):
    interp_irreg_1D(CMPs[:,col])

# Ajustando a escala de amostra para tempo
locks_t = np.linspace(0,nt,11)
labels_t = [0,0.2,0.4,0.6,0.8,1.0,1.2,1.4,1.6,1.8,2.0]

# Mostrando picks interpolados na vertical
plt.figure(3,figsize=(15,5))
plt.imshow(CMPs,aspect="auto")
cbar = plt.colorbar()
cbar.set_label("Velocidade RMS [m/s]",fontsize=15)
plt.title("Picks por CMP analisado",fontsize=20)
plt.xlabel("CMP analisado",fontsize=15)
plt.ylabel("Tempo [s]",fontsize=15)
plt.yticks(locks_t,labels_t)
plt.savefig("picksInterpVertical.png",dpi=200,bbox_inches="tight")

#%% Gerando modelo com todos os CMPs e interpolando poço a poço

# Preencendo os CMPs analizados no modelo completo
modelo_RMS[:,-1] = CMPs[:,-1]
for i in range(len(cmp_positions)):
    modelo_RMS[:,cmp_positions[i]] = CMPs[:,i]

# Interpolação 1D irregular poço a poço
for line in range(nt):
    interp_irreg_1D(modelo_RMS[line,:])

# Ajustando a escala para melhorar a visualização
locks_x = np.linspace(0,nx,7)
labels_x = np.linspace(0,nx,7,dtype=int)

# Mostrando o modelo completo
plt.figure(4,figsize=(15,5))
plt.imshow(modelo_RMS,aspect="auto")
cbar = plt.colorbar()
cbar.set_label("Velocidade RMS [m/s]",fontsize=15)
plt.title("Modelo usando os CMPs completos",fontsize=20)
plt.xlabel("CMPs",fontsize=15)
plt.ylabel("Tempo [s]",fontsize=15)
plt.yticks(locks_t,labels_t)
plt.xticks(locks_x,labels_x)
plt.savefig("modeloCompleto.png",dpi=200,bbox_inches="tight")
plt.show()

velRMS = modelo_RMS.T

velRMS.astype("float32",order="C").tofile("vrms_cmps_completos.bin")