import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

img = mpimg.imread("horizontes.png")

nx = img.shape[0] # Amostras em x no modelo 
nz = img.shape[1] # Amostras em z no modelo 

N = img[:nx,:nz,0].copy()

zhrz = []
xhrz = []

for j in range(len(N[0])):
    for i in range(1,len(N)):
        if N[i,j] < 1.0:
            xhrz.append(j) 
            zhrz.append(i)    
        
remove = []        
for i in range(1,len(zhrz)):
    if zhrz[i] == zhrz[i-1] + 1:
        remove.append(i)

for i in range(len(remove)):
    xhrz.pop(remove[i] - i)
    zhrz.pop(remove[i] - i)

hrz0 = []; xhrz0 = []
hrz1 = []; xhrz1 = []
hrz2 = []; xhrz2 = []
hrz3 = []; xhrz3 = []
hrz4 = []; xhrz4 = []
hrz5 = []; xhrz5 = []
hrz6 = []; xhrz6 = []
hrz7 = []; xhrz7 = []

xhrz = np.array(xhrz)
zhrz = np.array(zhrz)

x = np.arange(len(N[0]))

for i in range(len(x)):
    layers = np.where(xhrz == i)[0]

    hrz0.append(zhrz[layers[0]]); xhrz0.append(i)
    hrz1.append(zhrz[layers[1]]); xhrz1.append(i)
    hrz2.append(zhrz[layers[2]]); xhrz2.append(i)

    if i <= 1481:
        hrz3.append(zhrz[layers[3]]); xhrz3.append(i)
        hrz4.append(zhrz[layers[4]]); xhrz4.append(i)
        hrz5.append(zhrz[layers[5]]); xhrz5.append(i)
    
    if 1481 < i <= 1567:
        hrz4.append(zhrz[layers[3]]); xhrz4.append(i)  
        hrz5.append(zhrz[layers[4]]); xhrz5.append(i)  
        
    if i > 1567:
        hrz5.append(zhrz[layers[3]]); xhrz5.append(i)  

    if 102 <= i <= 1333: 
        hrz6.append(zhrz[layers[6]]); xhrz6.append(i) 
    
    if 1403 <= i <= 1482:
        hrz6.append(zhrz[layers[6]]); xhrz6.append(i) 
    
    if 1482 < i <= 1562:
        hrz6.append(zhrz[layers[5]]); xhrz6.append(i) 
        
    hrz7.append(zhrz[layers[-1]]); xhrz7.append(i)

np.array(hrz0).astype("int32",order="C").tofile("hrzs/zhrz0.bin")
np.array(hrz1).astype("int32",order="C").tofile("hrzs/zhrz1.bin")
np.array(hrz2).astype("int32",order="C").tofile("hrzs/zhrz2.bin")
np.array(hrz3).astype("int32",order="C").tofile("hrzs/zhrz3.bin")
np.array(hrz4).astype("int32",order="C").tofile("hrzs/zhrz4.bin")
np.array(hrz5).astype("int32",order="C").tofile("hrzs/zhrz5.bin")
np.array(hrz6).astype("int32",order="C").tofile("hrzs/zhrz6.bin")
np.array(hrz7).astype("int32",order="C").tofile("hrzs/zhrz7.bin")

np.array(xhrz0).astype("int32",order="C").tofile(f"hrzs/xhrz0_{len(xhrz0)}ams.bin")
np.array(xhrz1).astype("int32",order="C").tofile(f"hrzs/xhrz1_{len(xhrz1)}ams.bin")
np.array(xhrz2).astype("int32",order="C").tofile(f"hrzs/xhrz2_{len(xhrz2)}ams.bin")
np.array(xhrz3).astype("int32",order="C").tofile(f"hrzs/xhrz3_{len(xhrz3)}ams.bin")
np.array(xhrz4).astype("int32",order="C").tofile(f"hrzs/xhrz4_{len(xhrz4)}ams.bin")
np.array(xhrz5).astype("int32",order="C").tofile(f"hrzs/xhrz5_{len(xhrz5)}ams.bin")
np.array(xhrz6).astype("int32",order="C").tofile(f"hrzs/xhrz6_{len(xhrz6)}ams.bin")
np.array(xhrz7).astype("int32",order="C").tofile(f"hrzs/xhrz7_{len(xhrz7)}ams.bin")

plt.figure(1,figsize=(15,5))
plt.imshow(N[:-150,:]*np.nan, aspect="auto",cmap="Greys")
plt.scatter(xhrz,zhrz)
plt.scatter(xhrz0,hrz0)
plt.scatter(xhrz1,hrz1)
plt.scatter(xhrz2,hrz2)
plt.scatter(xhrz3,hrz3)
plt.scatter(xhrz4,hrz4)
plt.scatter(xhrz5,hrz5)
plt.scatter(xhrz6,hrz6)
plt.scatter(xhrz7,hrz7)
plt.show()
