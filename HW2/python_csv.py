import csv
import matplotlib.pyplot as plt

tA = [] # column 0
tB = [] # column 0
tC = [] # column 0
tD = [] # column 0

data1A = [] # column 1
#data2A = [] # column 2

data1B = [] # column 1
#data2B = [] # column 2

data1C = [] # column 1
#data2C = [] # column 2

data1D = [] # column 1
#data2D = [] # column 2

with open('sigA.csv') as f:
    # open the csv file
    reader = csv.reader(f)
    for row in reader:
        # read the rows 1 one by one
        tA.append(float(row[0])) # leftmost column
        data1A.append(float(row[1])) # second column
        #data2A.append(float(row[2])) # third column
with open('sigB.csv') as f:
    # open the csv file
    reader = csv.reader(f)
    for row in reader:
        # read the rows 1 one by one
        tB.append(float(row[0])) # leftmost column
        data1B.append(float(row[1])) # second column
        #data2B.append(float(row[2])) # third column

with open('sigC.csv') as f:
    # open the csv file
    reader = csv.reader(f)
    for row in reader:
        # read the rows 1 one by one
        tC.append(float(row[0])) # leftmost column
        data1C.append(float(row[1])) # second column
        #data2C.append(float(row[2])) # third column

with open('sigD.csv') as f:
    # open the csv file
    reader = csv.reader(f)
    for row in reader:
        # read the rows 1 one by one
        tD.append(float(row[0])) # leftmost column
        data1D.append(float(row[1])) # second column
        #data2D.append(float(row[2])) # third column

samp_rate = len(data1A)/tA[-1]
print(samp_rate)
# for i in range(len(tA)):
#      # print the data to verify it was read
#     print(str(tA[i]) + ", " + str(data1A[i]))
