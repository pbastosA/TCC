import sys
import segyio 
import numpy as np
import matplotlib.pyplot as plt

from skimage import exposure

def readBinaryArray(nPoints,filename):
    with open(filename, 'rb') as f:    
        array = np.fromfile(filename, dtype=np.int32, count=nPoints)
    return array

def readBinaryMatrix(dim1,dim2,filename):
    with open(filename, 'rb') as f:    
        data   = np.fromfile(filename, dtype=np.float32, count=dim1*dim2)
        matrix = np.reshape(data, [dim1,dim2], order='C')
    return matrix

def perc(matrix,value):
    p = np.percentile(matrix,[.5, value])
    image = exposure.rescale_intensity(matrix,in_range=(p[0],p[1]),out_range=(0,255))    
    return image

def mute(matrix,p):
    y = np.arange(p[0][1],p[1][1],dtype=int)
    x = np.array(((p[0][0] - p[1][0]) * y + p[1][0]*p[0][1] - p[0][0]*p[1][1]) / (p[0][1] - p[1][1]),dtype=int)
    for i in range(len(x)):
        matrix[y[i],x[i]:] = 0.0 

# Building header parameters 

nshots = 1064
spread = 320
nrecep = 1383

dx = 6.250
ds = 25

offsetMin = 100

recPositions = readBinaryArray(nrecep,"../parameters/xrec.bin")
srcPositions = readBinaryArray(nshots,"../parameters/xsrc.bin")

recElevation = np.zeros(len(recPositions))
srcElevation = np.zeros(len(srcPositions))

xsrc = np.zeros(nshots*spread)
zsrc = np.zeros(nshots*spread)
xrec = np.zeros(nshots*spread)
zrec = np.zeros(nshots*spread)
fldr = np.zeros(nshots*spread)
cdpt = np.zeros(nshots*spread)

for i in range(nshots):
    fold = slice(i*spread,i*spread+spread)
    
    xrec[fold] = np.flip(recPositions[i:i+spread]*dx) 
    zrec[fold] = recElevation[i:i+spread]
    
    xsrc[fold] = np.ones(spread)*srcPositions[i]*dx
    zsrc[fold] = np.ones(spread)*srcElevation[i]

    cdpt[fold] = np.arange(spread) + 1

    fldr[fold] = i + 1001

cmpx = np.array([])
cmpc = np.array([])

offset = xsrc - xrec
cmps = xsrc - (xsrc - xrec) / 2

for cmp in cmps:
    if cmp not in cmpx:
        cmpx = np.append(cmpx,cmp)
        cmpc = np.append(cmpc,len(np.where(cmp == cmps)[0]))

# reading seismic data

nt = 3000
dt = 0.0005

segyPath = "sintheticDataEngland.segy"

# Read seismic data
auxData = np.zeros((nt,nshots*spread),dtype=np.float32)
seismic = np.zeros((nt,nshots*spread),dtype=np.float32)

auxData = readBinaryMatrix(nshots*nt,spread,"sintheticDataEngland.bin")

for i in range(nshots):
    seismic[:,i*spread:i*spread + spread] = auxData[i*nt:i*nt + nt,::-1]

print("Dado importado")

seismicPerc = perc(seismic[:,500*spread:500*spread+spread],99)

tloc = np.linspace(0,nt,11)
tlab = np.around(tloc * dt, decimals=1)

xloc = np.linspace(0,spread,7)
xlab = np.around(xloc * ds,decimals=1)

plt.figure(1,figsize=(15,6))
plt.imshow(seismicPerc[:,:spread],aspect="auto",cmap="Greys")
plt.tight_layout()
plt.xticks(xloc,xlab)
plt.yticks(tloc,tlab)
plt.title("Sísmica sintética - Bruta",fontsize=18)
plt.xlabel("Distância [m]",fontsize=14)
plt.ylabel("Tempo [s]",fontsize=14)
plt.savefig("sismicaSinteticaBruta.png",dpi=200,bbox_inches="tight")

lag = 200   # Número de amostras da fonte dividido por 2
for i in range(nt-lag):
    seismic[i,:] = seismic[i+lag,:]
    seismicPerc[i,:] = seismicPerc[i+lag,:]

print("Lag da fonte corrigido")

plt.figure(2,figsize=(15,6))
plt.imshow(seismicPerc[:,:spread],aspect="auto",cmap="Greys")
plt.tight_layout()
plt.xticks(xloc,xlab)
plt.yticks(tloc,tlab)
plt.title("Sísmica sintética - atraso da fonte",fontsize=18)
plt.xlabel("Distância [m]",fontsize=14)
plt.ylabel("Tempo [s]",fontsize=14)
plt.savefig("sismicaLag.png",dpi=200,bbox_inches="tight")

points = [[0,150],[75,nt]]
for i in range(nshots):
    seismic[:150,i*spread:i*spread + spread] = 0.0
    seismic[nt-lag:,i*spread:i*spread + spread] = 5e-6
    mute(seismic[:,i*spread:i*spread + spread],points)

points = [[0,150],[75,nt]]
seismicPerc[:150,:] = 0.0
seismicPerc[nt-lag:,:] = 200
mute(seismicPerc,points)

print("Onda direta e refrações mutadas")

plt.figure(3,figsize=(15,6))
plt.imshow(seismicPerc[:,:spread],aspect="auto",cmap="Greys")
plt.tight_layout()
plt.xticks(xloc,xlab)
plt.yticks(tloc,tlab)
plt.title("Sísmica sintética - Refrações e onda direta",fontsize=18)
plt.xlabel("Distância [m]",fontsize=14)
plt.ylabel("Tempo [s]",fontsize=14)

plt.savefig("sismicaMute.png",dpi=200,bbox_inches="tight")
plt.show()
sys.exit()

# Create a segy from a 2D matrix
segyio.tools.from_array2D(segyPath,seismic.T)

# read empty segy
SEGY = segyio.open(segyPath,'r+',ignore_geometry=True)

# get binary header key
binheader = segyio.binfield.keys

# Edit binary header keys
SEGY.bin[segyio.BinField.Interval]              = int(dt*1e6)    #3217-3218* Sample interval in microseconds (µs). Mandatory for all data types.
SEGY.bin[segyio.BinField.IntervalOriginal]      = int(dt*1e6)    #3219-3220  Sample interval in microseconds (µs) of original field recording.
SEGY.bin[segyio.BinField.Format]                = 1              #3225-3226@ Data sample format code. Mandatory for all data. For ANP - BDEP it has to be = 1
SEGY.bin[segyio.BinField.SortingCode]           = 1              #3229-3230@ Trace sorting code
SEGY.bin[segyio.BinField.MeasurementSystem]     = 1              #3255-3256@ Measurement system: Highly recommended for all types of data. 1 = Meters 2 = Feet
SEGY.bin[segyio.BinField.ImpulseSignalPolarity] = 1              #3257-3258@ Impulse signal polarity 

# print binary header
# print("\n Check binary header \n")
# print("%25s %4s %5s \n" %("key","byte","value"))
# for k,v in binheader.items():    
#     print("%25s %d  %d" %(k,v,SEGY.bin[v]))

tracl = np.arange(nshots*spread) + 1

# set trace headers values
for idx, key in enumerate(SEGY.header):

    if idx % 100 == 0:    
        print(f"Preenchendo o header do traço {tracl[idx]}...")

    key.update({segyio.TraceField.TRACE_SEQUENCE_LINE            : int(tracl[idx])                  }) #1-4@     Trace sequence number within line (will increase if line continues on another reel) 
    key.update({segyio.TraceField.FieldRecord                    : int(fldr[idx])                   }) #9-12*    Original field record number
    key.update({segyio.TraceField.TraceNumber                    : int(tracl[idx])                  }) #13-16*   Trace number within original field record. It should be the field channel number
    key.update({segyio.TraceField.CDP                            : int(cmps[idx]*10)                }) #21-24@   CMP number
    key.update({segyio.TraceField.CDP_TRACE                      : int(cdpt[idx])                   }) #25-28    Trace number within the CDP ensemble (each ensemble starts with trace number one)
    key.update({segyio.TraceField.TraceIdentificationCode        : int(fldr[idx])                   }) #29-30*   Trace identification code:   
    key.update({segyio.TraceField.offset                         : int(offset[idx])                 }) #37-40@   Distance from source point to receiver group  
    key.update({segyio.TraceField.ReceiverGroupElevation         : int(zrec[idx])                   }) #41-44@   Receiver group elevation 
    key.update({segyio.TraceField.SourceSurfaceElevation         : int(zsrc[idx])                   }) #45-48@   Surface elevation at source 
    key.update({segyio.TraceField.ElevationScalar                : 1                                }) #69-70@   Scaler to be applied to all elevations and depths specified
    key.update({segyio.TraceField.SourceGroupScalar              : 1                                }) #71-72@   Scaler to be applied to all coordinates specified in bytes 73-88 to give real value.
    key.update({segyio.TraceField.SourceX                        : int(xsrc[idx])                   }) #73-76@   Source coordinate X.
    key.update({segyio.TraceField.SourceY                        : 0                                }) #77-80@   Source coordinate Y.
    key.update({segyio.TraceField.GroupX                         : int(xrec[idx])                   }) #81-84@   Group coordinate X. 
    key.update({segyio.TraceField.GroupY                         : 0                                }) #85-88@   Group coordinate Y.
    key.update({segyio.TraceField.CoordinateUnits                : 1                                }) #89-90@   Coordinate units. 1= length (meters or feet) 2= seconds of arc
    key.update({segyio.TraceField.TRACE_SAMPLE_INTERVAL          : int(dt*1e6)                      }) #117-118@ Sample interval in microseconds for this trace 
    key.update({segyio.TraceField.GainType                       : 1                                }) #119-120  Gain type of field instruments: 
    key.update({segyio.TraceField.TimeBaseCode                   : 1                                }) #167-168@ Time basis code: 1=local; 2=GMT; 3=other.
    key.update({segyio.TraceField.CDP_X                          : 0                                }) #181-184@ X coordinate for CDP. [I4]
    key.update({segyio.TraceField.CDP_Y                          : 0                                }) #185-188@ Y coordinate for CDP. [I4]
    
# get trace headers key
# traceheaders = segyio.tracefield.keys

# print trace header
# print("\n Check trace header \n")
# print("%40s %5s %6s %6s \n" %("Trace header ","byte","first","last"))
# for k,v in traceheaders.items():    
#     print("%40s %5d  %6d %6d " %(k,v,SEGY.attributes(v)[0],SEGY.attributes(v)[SEGY.tracecount-1]))

SEGY.close()
