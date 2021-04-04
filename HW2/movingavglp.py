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

def movavglp(dataarr,width):
    movarr = []
    for i in range(width,len(dataarr)):
        movarr.append(np.average(dataarr[i-width:i]))
    return movarr


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

movavgA = movavglp(dataA,100)
movavgB = movavglp(dataB,100)
movavgC = movavglp(dataC,100)
movavgD = movavglp(dataD,100)

frqAarrmv, dataAfftmv = data_fft(tA,movavgA)
frqBarrmv, dataBfftmv = data_fft(tB,movavgB)
frqCarrmv, dataCfftmv = data_fft(tC,movavgC)
frqDarrmv, dataDfftmv = data_fft(tD,movavgD)

fig, axs = plt.subplots(2, 2)
axs[0,0].loglog(frqAarr,abs(dataAfft),'black',label='Unfiltered')
axs[0,0].loglog(frqAarrmv,abs(dataAfftmv),'red',label='Filtered')
axs[0,0].legend()
axs[0,0].set_title('Moving Avg. Data A fft, 100 datapoint avg.')

axs[0,1].loglog(frqBarr,abs(dataBfft),'black', label='Unfiltered')
axs[0,1].loglog(frqBarrmv,abs(dataBfftmv),'red', label='Filtered')
axs[0,1].legend()
axs[0,1].set_title('Moving Avg. Data B fft, 100 datapoint avg.')

axs[1,0].loglog(frqCarr,abs(dataCfft),'black', label='Unfiltered')
axs[1,0].loglog(frqCarrmv,abs(dataCfftmv),'red', label='Filtered')
axs[1,0].legend()
axs[1,0].set_title('Moving Avg. Data C fft, 100 datapoint avg.')

axs[1,1].loglog(frqDarr,abs(dataDfft),'black', label='Unfiltered')
axs[1,1].loglog(frqDarrmv,abs(dataDfftmv),'red', label='Filtered')
axs[1,1].legend()
axs[1,1].set_title('Moving Avg. Data D fft, 100 datapoint avg.')
#axs[0,0].plot(frqAarrmv,'b')
fig.tight_layout(pad=1.0)
plt.show()
