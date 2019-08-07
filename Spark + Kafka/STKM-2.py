from __future__ import print_function

from pyspark import SparkContext

import pyspark

import sys

from pymongo import MongoClient

from pyspark.streaming import StreamingContext

from pyspark.streaming.kafka import KafkaUtils

from pyspark.mllib.clustering import StreamingKMeansModel, StreamingKMeans

from json import loads

from pyspark.mllib.linalg import Vectors

sc = SparkContext(appName="StreamingKMeans")
ssc = StreamingContext(sc,10)
ssc.checkpoint("/tmp/checkpoints/")


initialCenters = [
[604328, 574379],
[801908, 318382 ],
[416383, 786204 ],
[822771, 732034 ],
[850993, 157873 ],
[338586, 563537 ],
[169274, 348574 ],
[619259, 397671 ],
[241071, 844424 ],
[321801, 165319 ],
[139493, 557352 ],
[508785, 174800 ],
[398934, 404142 ],
[860858, 546059 ],
[674365, 860464 ]
]

initialWeights = [1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0]

stkm = StreamingKMeans(k=sys.argv[1],decayFactor=1.0).setInitialCenters([[500,500],[600,600]],[1.0,1.0])


directKafkaStream = KafkaUtils.createDirectStream(ssc, ['StreamingKMeansTFG'], {"metadata.broker.list":"localhost:9092","auto_offset_reset":'earliest'})

parsed = directKafkaStream.map(lambda v: loads(v[1]))

parsed = parsed.map(lambda line: Vectors.dense([float(x) for x in line.strip().split()]))

stkm.trainOn(parsed)

def sendPartition(rdd):
    connection     = MongoClient("mongodb://localhost:27017/")
    test_db        = connection.get_database('sparkDB')
    collection = test_db.get_collection('sset1')
    model = stkm.latestModel()
    centers = model.centers
    weights = model.clusterWeights
    myquery = { "name": "sset1" }
    newvalues = { "$set": { "clusterCenters": centers.tolist(),"clusterWeights":weights } }
    collection.update_one(myquery, newvalues)
    connection.close()


parsed.count().foreachRDD(sendPartition)

stkm.predictOn(parsed).pprint()

parsed.count().pprint()

ssc.start()
ssc.awaitTermination()
