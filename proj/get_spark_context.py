import findspark
import pyspark
from pyspark import SparkConf, SparkContext
from pyspark.sql import SparkSession, SQLContext

findspark.init()
findspark.find()


def get_spark_sql_context():
    conf = SparkConf().setAll([("spark.worker.cleanup.enabled", True),
                               ("spark.serializer",
                                "org.apache.spark.serializer.KryoSerializer"),
                               ("spark.kryo.registrationRequired", "false"),
                               ("spark.master", "spark://s01:7077")])

    # sc = SparkContext(conf=conf).getOrCreate()
    sc = pyspark.SparkContext.getOrCreate(conf=conf)
    sc.setLogLevel("WARN")
    spark = SparkSession \
        .builder \
        .master('spark://s01:7077') \
        .appName('Big Data Project') \
        .config('spark.sql.debug.maxToStringFields', 2000) \
        .config('spark.debug.maxToStringFields', 2000) \
        .getOrCreate()
    sc.addPyFile('data_manipulation.py')
    sqlContext = SQLContext(sc)
    return [spark, sqlContext]


# def get_spark_sql_context():
#     conf = SparkConf().setAll([("spark.worker.cleanup.enabled", False),
#                                ("spark.serializer",
#                                 "org.apache.spark.serializer.KryoSerializer"),
#                                ("spark.kryo.registrationRequired", "false"),
#                                ("spark.master", "local")])

#     # sc = SparkContext(conf=conf).getOrCreate()
#     sc = pyspark.SparkContext.getOrCreate(conf=conf)
#     sc.setLogLevel("WARN")
#     spark = SparkSession \
#         .builder \
#         .master('local') \
#         .appName('Big Data Project') \
#         .config('spark.sql.debug.maxToStringFields', 2000) \
#         .config('spark.debug.maxToStringFields', 2000) \
#         .getOrCreate()
#     sc.addPyFile('data_manipulation.py')
#     sqlContext = SQLContext(sc)
#     return [spark, sqlContext]