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
uberCollection = test_db.get_collection("UberPredictions")

colors = ['r', 'k', 'b','grey','darkorange','m','y','c','gold','slateblue','beige','coral','g','peru','pink']

cursor = collection.find({})


if cursor.count()==0:
   logging.error("La coleccion "+sys.argv[1]+" no existe")

else:

     truePredictions = []

     points = []

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

     with open("datasets/UberData.txt","r") as file:
          i = 0
          for line in file:
              line = line.split()
              document = {
                      "lat":line[1],
                      "long":line[2],
                      "hour": line[0],
                      "cluster":predictions[i]
                      }
              i = i + 1
              uberCollection.insert(document)

     for i in range(0,len(points)):
         x = points[i][0]
         y = points[i][1]
         plt.plot(float(x), float(y), 'o',markersize=2, color=colors[predictions[i]])
     plt.show()



