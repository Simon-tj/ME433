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

iirA = iirfilt(dataA,0.90,0.10)
iirB = iirfilt(dataB,0.95,0.05)
iirC = iirfilt(dataC,0.95,0.05)
iirD = iirfilt(dataD,0.98,0.02)

frqAarriir, dataAfftiir = data_fft(tA,iirA)
frqBarriir, dataBfftiir = data_fft(tB,iirB)
frqCarriir, dataCfftiir = data_fft(tC,iirC)
frqDarriir, dataDfftiir = data_fft(tD,iirD)

fig, axs = plt.subplots(2, 2)
axs[0,0].loglog(frqAarr,abs(dataAfft),'black',label='Unfiltered')
axs[0,0].loglog(frqAarriir,abs(dataAfftiir),'red',label='Filtered')
axs[0,0].legend()
axs[0,0].set_title('IIR Filter Data A fft (A = 0.90, B = 0.10)')

axs[0,1].loglog(frqBarr,abs(dataBfft),'black', label='Unfiltered')
axs[0,1].loglog(frqBarriir,abs(dataBfftiir),'red', label='Filtered')
axs[0,1].legend()
axs[0,1].set_title('IIR Filter Data B fft (A = 0.95, B = 0.05)')

axs[1,0].loglog(frqCarr,abs(dataCfft),'black', label='Unfiltered')
axs[1,0].loglog(frqCarriir,abs(dataCfftiir),'red', label='Filtered')
axs[1,0].legend()
axs[1,0].set_title('IIR Filter Data C fft (A = 0.95, B = 0.05)')

axs[1,1].loglog(frqDarr,abs(dataDfft),'black', label='Unfiltered')
axs[1,1].loglog(frqDarriir,abs(dataDfftiir),'red', label='Filtered')
axs[1,1].legend()
axs[1,1].set_title('IIR Filter Data D fft (A = 0.98, B = 0.02)')
#axs[0,0].plot(frqAarrmv,'b')
fig.tight_layout(pad=1.0)
plt.show()
