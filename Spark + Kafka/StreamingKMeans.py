from __future__ import print_function

from pyspark import SparkContext

import pyspark

import sys

import logging

from pymongo import MongoClient

from pyspark.streaming import StreamingContext

from pyspark.streaming.kafka import KafkaUtils

from pyspark.mllib.clustering import StreamingKMeansModel, StreamingKMeans

from json import loads

import sys

from pyspark.mllib.linalg import Vectors

logging.basicConfig(level=logging.INFO)

sc = SparkContext(appName="StreamingKMeans")
ssc = StreamingContext(sc,10)
ssc.checkpoint("/tmp/checkpoints/")

with open(sys.argv[1],"r") as file:
     parameters = []
     for param in file:
         parameters.append(param.strip())

with open(sys.argv[2],"r") as file:
     initialCenters = []
     for center in file:
         initialCenters.append(center.split())

logging.info(initialCenters)

initialWeights = []
for i in initialCenters:
    initialWeights.append(1.0)

config = sc.broadcast(parameters)
numberClusters = config.value[0]
mongoIP = config.value[1]
mongoDataBase = config.value[2]
mongoCollection = config.value[3]


stkm = StreamingKMeans(k=numberClusters,decayFactor=1).setInitialCenters(initialCenters,initialWeights)

#stkm = StreamingKMeans(k=int(numberClusters),decayFactor=1.0).setRandomCenters(2,1.0,100)

directKafkaStream = KafkaUtils.createDirectStream(ssc, ['StreamingKMeansTFG'], {"metadata.broker.list":"localhost:9092","auto_offset_reset":'earliest'})

parsed = directKafkaStream.map(lambda v: loads(v[1]))

parsed = parsed.map(lambda line: Vectors.dense([float(x) for x in line.strip().split()]))

stkm.trainOn(parsed)

def sendPartition(rdd):
    connection     = MongoClient(mongoIP)
    test_db        = connection.get_database(mongoDataBase)
    collection = test_db.get_collection(mongoCollection)
    model = stkm.latestModel()
    centers = model.centers
    weights = model.clusterWeights
    myquery = { "name": mongoCollection}
    newvalues = { "$set": { "clusterCenters": centers.tolist(),"clusterWeights":weights } }
    result = collection.update_one(myquery, newvalues)
    logging.info("Se han actualizado "+str(result.modified_count)+" elementos en MongoDB")
    connection.close()


parsed.count().foreachRDD(sendPartition)

parsed.count().pprint()

ssc.start()
ssc.awaitTermination()
