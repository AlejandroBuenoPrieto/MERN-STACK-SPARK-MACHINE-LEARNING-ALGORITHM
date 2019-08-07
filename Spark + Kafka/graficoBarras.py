import numpy as np
import matplotlib.pyplot as plt
plt.style.use('ggplot')


f1 = open("asset1ResultadosCentersOriginales.txt","r")
f2 = open("asset1ResultadosCentersSpark.txt","r")
f3 = open("asset1Resultados.txt","r")
labels = ['SparkRandom', 'RandomData1', 'RandomData2']

randomSpark = []

randomDataSet = []

originalDataSet = []

for line in f1:
    line = line.split()
    originalDataSet.append(float(line[len(line)-1]))
for line in f2:
    line = line.split()
    randomSpark.append(float(line[len(line)-1]))
for line in f3:
    line = line.split()
    randomDataSet.append(float(line[len(line)-1]))


X = np.arange(3)
datos = []
datos.append(originalDataSet)
datos.append(randomDataSet)
datos.append(randomSpark)

plt.bar(X + 0.00, datos[0], color = "darkorange", width = 0.15,label="Random2")
plt.bar(X + 0.25, datos[1], color = "navy", width = 0.15,label="Random1")
plt.bar(X + 0.50, datos[2], color = "gold", width = 0.15,label="SparkRandom")
plt.xticks(X+0.38, ["Recall","Precision","F1-Score"])

ax = plt.gca()
plt.legend(bbox_to_anchor=(1.1, 1.1), bbox_transform=ax.transAxes)

plt.show()
