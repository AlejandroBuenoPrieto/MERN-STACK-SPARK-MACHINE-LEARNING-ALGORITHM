from kafka import KafkaProducer
import json
import time
from json import dumps
import sys
import logging
from os import path

logging.basicConfig(level=logging.INFO)
logging.info("Generador de data streams iniciado")

if path.exists(sys.argv[1]):
   file = open(sys.argv[1],"r")

   producer = KafkaProducer(bootstrap_servers='localhost:9092',value_serializer=lambda x: 
                         dumps(x).encode('utf-8'))
   for line in file:
       line = line.replace("\t"," ")
       line = line.replace("\n","")
       line = line.replace("\"" , "")
       producer.send('StreamingKMeansTFG', line)
       time.sleep(float(sys.argv[2]))
   logging.info("El dataset ha sido enviado correctamente")
else:
    logging.error("El fichero "+sys.argv[1]+" no existe")
