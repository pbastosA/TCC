import numpy as np

def gerar_matriz (n_linhas, n_colunas):
    matriz = []

    for _ in range(n_linhas):
        matriz.append( [" "] * n_colunas )

    return matriz

cdp_min = 80125 
cdp_max = 306250
cdps = np.arange(cdp_min,cdp_max,125)

# print(len(cdps),cdps[0],cdps[-1])

esp = 180 # espaçamento entre cmps completos
l = 5     # Número de linhas para colar no iva.sh

velan = cdps[::esp]

cmp_iva = gerar_matriz(l,int(len(velan)/l))

index = 0
for j in range(len(cmp_iva[0])):
    for i in range(l):
        cmp_iva[i][j] = "cmp"+str(index+1)+"="+str(velan[int(index)])
        index += 1

cmp_iva = np.array(cmp_iva)

np.savetxt("cmps.txt",cmp_iva,fmt="%s")
