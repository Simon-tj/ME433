#Choosing a cutoff frequency of 100 Hz for the FIR filt

import matplotlib.pyplot as plt
import numpy as np
import csv

tA = [] # column 0
tB = [] # column 0
tC = [] # column 0
tD = [] # column 0

dataA = [] # column 1
dataB = [] # column 1
dataC = [] # column 1
dataD = [] # column 1

def csv_read(csvstr, tarr, dataarr):
    with open(csvstr) as f:
        # open the csv file
        reader = csv.reader(f)
        for row in reader:
            # read the rows 1 one by one
            tarr.append(float(row[0])) # leftmost column
            dataarr.append(float(row[1])) # second column

def mafilt(dataarr,width):
    movarr = []
    for i in range(width,len(dataarr)):
        movarr.append(np.average(dataarr[i-width:i]))
    return movarr

def iirfilt(dataarr,A,B):
    iirarr = [0]
    for i in range(1,len(dataarr)-1):
        iirarr.append(A*iirarr[i-1] + B*dataarr[i])
    return iirarr

def firfilt(dataarr):
    coeff = np.array([
    0.050864468366675471,
    0.051447898537001137,
    0.051965975783172462,
    0.052417478485077405,
    0.052801340859369245,
    0.053116655958639653,
    0.053362678224921099,
    0.053538825589686409,
    0.053644681113902914,
    0.053679994163108466,
    0.053644681113902914,
    0.053538825589686409,
    0.053362678224921099,
    0.053116655958639653,
    0.052801340859369245,
    0.052417478485077405,
    0.051965975783172462,
    0.051447898537001137,
    0.050864468366675471,
    ])

    firarr = []
    for i in range(len(coeff),len(dataarr)):
        firarr.append(sum(coeff*dataarr[i-len(coeff):i]))
    return firarr


def data_fft(tarr,dataarr):
    Fs = 10000 # sample rate
    Ts = 1.0/Fs; # sampling interval
    ts = np.arange(0,tarr[-1],Ts) # time vector
    y = dataarr # the data to make the fft from
    n = len(y) # length of the signal
    k = np.arange(n)
    T = n/Fs
    frq = k/T # two sides frequency range
    frq = frq[range(int(n/2))] # one side frequency range
    Y = np.fft.fft(y)/n # fft computing and normalization
    Y = Y[range(int(n/2))]
    frqarr = frq
    fftarr = Y

    return frqarr, fftarr
csv_read('SigA.csv',tA,dataA)
csv_read('SigB.csv',tB,dataB)
csv_read('SigC.csv',tC,dataC)
csv_read('SigD.csv',tD,dataD)

frqAarr, dataAfft = data_fft(tA,dataA)
frqBarr, dataBfft = data_fft(tB,dataB)
frqCarr, dataCfft = data_fft(tC,dataC)
frqDarr, dataDfft = data_fft(tD,dataD)

firA = firfilt(dataA)
firB = firfilt(dataB)
firC = firfilt(dataC)
firD = firfilt(dataD)

frqAarrfir, dataAfftfir = data_fft(tA,firA)
frqBarrfir, dataBfftfir = data_fft(tB,firB)
frqCarrfir, dataCfftfir = data_fft(tC,firC)
frqDarrfir, dataDfftfir = data_fft(tD,firD)

fig, axs = plt.subplots(2, 2)
axs[0,0].loglog(frqAarr,abs(dataAfft),'black',label='Unfiltered')
axs[0,0].loglog(frqAarrfir,abs(dataAfftfir),'red',label='Filtered')
axs[0,0].legend()
axs[0,0].set_title('FIR Filter Data A fft')

axs[0,1].loglog(frqBarr,abs(dataBfft),'black', label='Unfiltered')
axs[0,1].loglog(frqBarrfir,abs(dataBfftfir),'red', label='Filtered')
axs[0,1].legend()
axs[0,1].set_title('FIR Filter Data B fft')

axs[1,0].loglog(frqCarr,abs(dataCfft),'black', label='Unfiltered')
axs[1,0].loglog(frqCarrfir,abs(dataCfftfir),'red', label='Filtered')
axs[1,0].legend()
axs[1,0].set_title('FIR Filter Data C fft')

axs[1,1].loglog(frqDarr,abs(dataDfft),'black', label='Unfiltered')
axs[1,1].loglog(frqDarrfir,abs(dataDfftfir),'red', label='Filtered')
axs[1,1].legend()
axs[1,1].set_title('FIR Filter Data D fft')
#axs[0,0].plot(frqAarrmv,'b')
fig.tight_layout(pad=1.0)
#plt.title('h = [0.050864468366675471,0.051447898537001137,0.051965975783172462,0.052417478485077405,0.052801340859369245,0.053116655958639653,0.053362678224921099,0.053538825589686409,0.053644681113902914,0.053679994163108466,0.053644681113902914,0.053538825589686409,0.053362678224921099,0.053116655958639653,0.052801340859369245,0.052417478485077405,0.051965975783172462,0.051447898537001137,0.050864468366675471,]')
plt.show()
