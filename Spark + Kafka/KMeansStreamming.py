from pyspark import SparkContext

from pyspark.streaming import StreamingContext

from pyspark.streaming.kafka import KafkaUtils

from pyspark.mllib.clustering import KMeansModel, StreamingKMeansModel

from kafka import KafkaConsumer

from pyspark.mllib.linalg import Vectors

import matplotlib.pyplot as plt

from json import loads

import os

os.environ['PYSPARK_SUBMIT_ARGS'] = '--packages org.apache.spark:spark-streaming-kafka-0-8_2.11:2.0.2 pyspark-shell'

sc = SparkContext(appName="PythonSparkStreamingKafka")

sc.setLogLevel("WARN")

ssc = StreamingContext(sc,120)

initWeights = [1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0]

offlineModel = KMeansModel.load(sc,"KMeansModel")

stkm = StreamingKMeansModel(offlineModel.clusterCenters,initWeights)

#kafkaStream = KafkaUtils.createDirectStream(ssc, ['test'], {'metadata.broker.list': 'localhost:9092'})

#lines = kafkaStream.map(lambda line: array([float(x) for x in line.split('\t')]))

consumer = KafkaConsumer ('test',
     bootstrap_servers =[ 'localhost:9092'],
     value_deserializer=lambda x: loads(x.decode('utf-8')),consumer_timeout_ms=10000)

colors = ['r', 'k', 'b','grey','darkorange','m','y','c','gold','slateblue','beige','coral','g','peru','pink']

i=0

print("Collecting data")
for message in consumer:
    testData = Vectors.dense([float(x) for x in message.value.strip().split()])
    plt.plot(testData[0], testData[1], 'o', color=colors[stkm.predict(testData)])
print("Vamos a dibujar")
plt.show()

ssc.start()
ssc.awaitTermination()
