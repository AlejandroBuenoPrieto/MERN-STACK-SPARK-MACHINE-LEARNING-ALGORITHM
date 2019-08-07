import numpy as np
import matplotlib.pyplot as plt
plt.style.use('ggplot')


f1 = open("asset1ResultadosDecayFactor0.txt","r")
f4 = open("asset1ResultadosDecayFactor0.25.txt","r")
f3 = open("asset1ResultadosDecayFactor0.5.txt","r")
f2 = open("asset1Resultados.txt","r")
labels = ['SparkRandom', 'RandomData1', 'RandomData2']

decay0 = []

decay025 = []

decay05 = []

decay1 = []

for line in f1:
    line = line.split()
    decay0.append(float(line[len(line)-1]))
for line in f2:
    line = line.split()
    decay025.append(float(line[len(line)-1]))
for line in f3:
    line = line.split()
    decay05.append(float(line[len(line)-1]))
for line in f4:
    line = line.split()
    decay1.append(float(line[len(line)-1]))

y = [0,0.25,0.5,1]
d = []
labels = ["recall","precision","F1-Score"]
for i in range(0,len(decay1)):
    d.append(decay0[i])
    d.append(decay025[i])
    d.append(decay05[i])
    d.append(decay1[i])
    plt.plot(y,d, '-o',markersize=5,label=labels[i])
    d = []
plt.legend()
plt.show()

