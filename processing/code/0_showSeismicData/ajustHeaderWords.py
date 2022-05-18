import numpy as np

#%% Calculando o fldr

# ffid = np.arange(1001,2065,1,dtype=int)

# fldr = np.array([],dtype=int)

# for i in range(320):
#     fldr = np.append(fldr,ffid)

# np.savetxt("fldr.txt",fldr,fmt="%.0f")

#%% Calculando o offset

# offset = np.arange(100,8100,25)

# key = np.zeros(340480)
# cont = 0
# for i in range(340480):
    
#     if i % 1064 == 0:
#         offset_atual = offset[cont]
#         cont += 1

#     key[i] = offset_atual

# np.savetxt("offset.txt",key,fmt="%.0f")

#%% Calculando o cdpt

# data = np.loadtxt("keyHeaderWords.txt",dtype=str)

# cdpt = np.zeros(len(data),dtype=int)

# for i in range(len(data)):
    # cdpt[i] = int(data[i][3][5:]))
    # if i % 10000 == 0:
    #     print(f"Já escrevi {i} componentes!")

# np.savetxt("cdpt.txt",cdpt,fmt="%.0f")

#%% Separar chaves do arquivo corrigido para adicionar no dado original

data = np.loadtxt("parametros_corrigidos.txt",dtype=str)

fldr = np.zeros(len(data),dtype=int)
offset = np.zeros(len(data),dtype=int)
cdp = np.zeros(len(data),dtype=int)
cdpt = np.zeros(len(data),dtype=int)

for i in range(len(data)):
    fldr[i] = int(data[i][1][5:])
    offset[i] = int(data[i][2][7:])
    cdp[i] = int(data[i][3][4:])
    cdpt[i] = int(data[i][4][5:])


np.savetxt("fldr.txt",fldr,fmt="%.0f")
np.savetxt("offset.txt",offset,fmt="%.0f")
np.savetxt("cdp.txt",cdp,fmt="%.0f")
np.savetxt("cdpt.txt",cdpt,fmt="%.0f")
