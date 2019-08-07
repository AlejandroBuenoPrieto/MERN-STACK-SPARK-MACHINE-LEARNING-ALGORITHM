from sklearn.metrics import recall_score
from sklearn.metrics import precision_score
from pyspark.mllib.clustering import StreamingKMeansModel
from pyspark import SparkContext
from pyspark.mllib.evaluation import MulticlassMetrics
from pymongo import MongoClient
import matplotlib.pyplot as plt
plt.style.use('ggplot')
import sys
import logging
logging.basicConfig(level=logging.INFO)

logging.info("Se ha inciado Cluster Evaluator")

sc = SparkContext(appName="ClusterEvaluator")

connection     = MongoClient("mongodb://localhost:27017/")
test_db        = connection.get_database('SparkStreamingDB')
collection = test_db.get_collection(sys.argv[1])

colors = ['r', 'k', 'b','grey','darkorange','m','y','c','gold','slateblue','beige','coral','g','peru','pink','brown','wheat','salmon','teal','plum']

cursor = collection.find({})

if cursor.count()==0:
   logging.error("La coleccion "+sys.argv[1]+" no existe")

else:

     truePredictions = []

     points = []

     with open("trueground/trueground"+sys.argv[1]+".txt", "r") as fichero:
    	  for linea in fichero:
              c = linea.strip("\n").split()
              if sys.argv[1]==("sset1"):
                 truePredictions.append(int(c[0])-1)
              if sys.argv[1]==("asset1"):
                 truePredictions.append(int(c[0])-1)
              else:
                 truePredictions.append(int(c[0]))

     with open("datasets/"+sys.argv[1]+".txt","r") as fichero:
    	  for linea in fichero:
              points.append(linea.strip("\n").split())

     for document in cursor:
         centers = document["clusterCenters"]
         weights = document["clusterWeights"]

     stkm = StreamingKMeansModel(centers, weights)

     predictions = []

     for point in points:
         predictions.append(stkm.predict(point))

     recall = recall_score(truePredictions,predictions, average='weighted')

     precision = precision_score(truePredictions, predictions, average='weighted')

     f1Score = 2 * (precision * recall) / (precision + recall)

     logging.info("Recall = " + str(recall) )
     logging.info("Precision = " + str(precision) )
     logging.info("F1-Score = " + str(f1Score))

     f=open(sys.argv[1]+"Resultados.txt","w")
     f.write("Recall = " + str(recall))
     f.write("\n") 
     f.write("Precision = " + str(precision))
     f.write("\n")
     f.write("F1-Score = " + str(f1Score))
     for i in range(0,len(points)):
         x = points[i][0]
         y = points[i][1]
         plt.plot(int(x), int(y), 'o',markersize=2, color=colors[predictions[i]])
     
     plt.title(sys.argv[1])
     plt.ylabel("Valores de y")
     plt.xlabel("Valores de x")
     plt.show()



