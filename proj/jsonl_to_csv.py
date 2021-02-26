import findspark
findspark.init()
findspark.find()
import pyspark
findspark.find()
import os
import re

from pyspark import SparkContext, SparkConf
from pyspark.sql import SparkSession
from pyspark.sql.types import StructType, StringType, FloatType, StructField

#   Initialize the Spark session
conf = pyspark.SparkConf().setAppName('appName').setMaster('local')
sc = pyspark.SparkContext(conf=conf)

#Imports for pysparksql
from pyspark.sql import SQLContext
from pyspark.sql.functions import *

source_path = r"C:\Users\Davide\id_tweets\hydrated_tweets_01.jsonl"
sqlContext = SQLContext(sc)

df = sqlContext.read.json(source_path)
df_small = df.select('full_text', 'id_str', 'created_at')

df_small.coalesce(1).write.option("header", "true").option("delimiter", "\t").csv("name.csv")

dim_dataset = 30
for i in range(1, dim_dataset+1):
    if i < 10:
        ind = '0' + str(i)
    else:
        ind = str(i)
    source_path = r"C:\Users\Davide\id_tweets\hydrated_tweets_" + ind + ".csv"
    for filename in os.listdir(source_path):
        if re.match("part-.+[.csv]$", filename):
            print("match")
            new_path = r"C:\Users\Davide\id_tweets\hydrated_tweets_csv"
            new_name = r"hydrated_tweets_" + ind + ".csv"
            os.rename(os.path.join(source_path,filename), os.path.join(new_path, new_name))