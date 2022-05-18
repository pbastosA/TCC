import numpy as np
import matplotlib.pyplot as plt

ng = 320       # Quantidade de sensores ativos por tiro
dg = 25        # Espaçamento entre os sensores

ns = 1064      # Quantidade de fontes na aquisição
offset = 100   # Distância entre a fonte e o sensor mais próximo
ds = 25        # Espaçamento entre disparos  

sx = np.zeros(ng*ns)
gx = np.zeros(ng*ns)
id = np.zeros(ng*ns)

gx[:ng] = np.arange(ng) * dg
sx[:ng] = np.ones(ng) * (ng-1) * dg + offset
id[:ng] = np.ones(ng)

for i in range(1,ns):
    gx[i*ng:i*ng + ng] = gx[:ng] + i*ds
    sx[i*ng:i*ng + ng] = sx[:ng] + i*ds
    id[i*ng:i*ng + ng] = i+1

cmpx = np.array([])
cmpc = np.array([])

cmps = sx - (sx - gx) / 2
for cmp in cmps:
    if cmp not in cmpx:
        cmpx = np.append(cmpx,cmp)
        cmpc = np.append(cmpc,len(np.where(cmp == cmps)[0]))

plt.figure(1,figsize=(12,7))
plt.subplot(211)
plt.scatter(gx,id)
plt.scatter(sx,id)
plt.scatter(cmpx,np.ones(len(cmpx))*ns+100)
plt.gca().invert_yaxis()
plt.xlim([-1000,36000])
#plt.gca().set_xticklabels([])
plt.title(f"Geometria com {ng*ns} traços no total")
plt.ylabel("Identificador de fontes")
plt.legend(["Receptores","Fontes","Pontos médios"],loc="upper right")

plt.subplot(212)
# plt.stem(cmpx,cmpc,use_line_collection=True)

cmpCompleto = np.arange(8012.5,30650,12.5)
tracrCMP = np.ones(len(cmpCompleto))*160  
plt.stem(cmpCompleto[::80],tracrCMP[::80],use_line_collection=True)
plt.xlim([-1000,36000])
plt.grid(axis="y")
plt.xlabel("Distância [m]")
plt.ylabel("Traços por CMP")
plt.savefig("cmpTraceCountVelAn.png",dpi=200,bbox_inches="tight")
plt.show()
