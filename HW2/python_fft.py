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

csv_read('SigA.csv',tA,dataA)
csv_read('SigB.csv',tB,dataB)
csv_read('SigC.csv',tC,dataC)
csv_read('SigD.csv',tD,dataD)

# dt = 1.0/10000.0 # 10kHz
# t = np.arange(0.0, 1.0, dt) # 10s
# # a constant plus 100Hz and 1000Hz
# s = 4.0 * np.sin(2 * np.pi * 100 * t) + 0.25 * np.sin(2 * np.pi * 1000 * t) + 25

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

frqAarr, dataAfft = data_fft(tA,dataA)
frqBarr, dataBfft = data_fft(tB,dataB)
frqCarr, dataCfft = data_fft(tC,dataC)
frqDarr, dataDfft = data_fft(tD,dataD)

fig, axs = plt.subplots(4, 2)

axs[0,0].plot(tA,dataA,'b')
axs[0,0].set_xlabel('Time')
axs[0,0].set_ylabel('Amplitude')
axs[1,0].loglog(frqAarr,abs(dataAfft),'b') # plotting the fft
axs[1,0].set_xlabel('Freq (Hz)')
axs[1,0].set_ylabel('|Y(freq)|')
axs[0,0].set_title('Sig A Data')

axs[0,1].plot(tB,dataB,'b')
axs[0,1].set_xlabel('Time')
axs[0,1].set_ylabel('Amplitude')
axs[1,1].loglog(frqBarr,abs(dataBfft),'r') # plotting the fft
axs[1,1].set_xlabel('Freq (Hz)')
axs[1,1].set_ylabel('|Y(freq)|')
axs[0,1].set_title('Sig B Data')

axs[2,0].plot(tC,dataC,'b')
axs[2,0].set_xlabel('Time')
axs[2,0].set_ylabel('Amplitude')
axs[3,0].loglog(frqCarr,abs(dataCfft),'g') # plotting the fft
axs[3,0].set_xlabel('Freq (Hz)')
axs[3,0].set_ylabel('|Y(freq)|')
axs[2,0].set_title('Sig C Data')

axs[2,1].plot(tD,dataD,'b')
axs[2,1].set_xlabel('Time')
axs[2,1].set_ylabel('Amplitude')
axs[3,1].loglog(frqDarr,abs(dataDfft),'y') # plotting the fft
axs[3,1].set_xlabel('Freq (Hz)')
axs[3,1].set_ylabel('|Y(freq)|')
axs[2,1].set_title('Sig D Data')

plt.show()
