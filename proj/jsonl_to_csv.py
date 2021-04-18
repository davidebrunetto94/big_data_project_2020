import findspark
findspark.init()
findspark.find()
import pyspark
import os
import re
import shutil
from pyspark import SparkContext, SparkConf
from pyspark.sql import SparkSession
from pyspark.sql.types import StructType, StringType, FloatType, StructField

findspark.init()
findspark.find()

#   Initialize the Spark session
conf = pyspark.SparkConf().setAppName('appName').setMaster('local')
sc = pyspark.SparkContext(conf=conf)

#Imports for pysparksql
from pyspark.sql import SQLContext
from pyspark.sql.functions import *
sqlContext = SQLContext(sc)

dim_dataset = 30
#If you launch the script in the directory with the files, you can leave this as it is, otherwise you have to specify the path
source_path = r"./"

for i in range(1, dim_dataset+1):
    if i < 10:
        ind = '0' + str(i)
    else:
        ind = str(i)
    source_file = source_path + "hydrated_tweets_" + ind + ".jsonl"
    df = sqlContext.read.json(source_file)
    #create a new df with only the selected fields
    df_small = df.select('full_text', 'id_str', 'created_at')
    folder_name = "name" + ind + ".csv"
    #write them
    df_small.coalesce(1).write.option("header", "true").option("delimiter", "\t").csv(folder_name)
    target_folder = os.path.join(source_path,folder_name)
    for filename in os.listdir(target_folder):
        if re.match("part-.+[.csv]$", filename):
            print("-----------------MATCHHHHHH----------")
            new_path = r"./"
            new_name = "hydrated_tweets_" + ind + ".csv"
            os.rename(os.path.join(target_folder,filename), os.path.join(new_path, new_name))
            shutil.rmtree(target_folder, ignore_errors=True)