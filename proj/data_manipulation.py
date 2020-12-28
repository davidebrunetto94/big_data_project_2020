from pyspark import SparkContext, SparkConf
from pyspark.sql import SparkSession
from pyspark.sql.types import StructType, StringType, FloatType, StructField, IntegerType
from pyspark.sql import SQLContext
from pyspark.sql.functions import regexp_replace, col
import pyspark
import findspark
findspark.init()
findspark.find()

# This function initializes the sparkContext and sparkSession, creates two dataframes, one for the hydrated tweets and
# one for the tweets id, joins them and then uses regular expression to "clean them"


def get_clean_data():
    #   Initialize the Spark session
    conf = pyspark.SparkConf().setAppName('appName').setMaster('local')
    sc = pyspark.SparkContext(conf=conf)
    spark = SparkSession \
        .builder \
        .master('local') \
        .appName('Notebook') \
        .config('spark.sql.debug.maxToStringFields', 2000) \
        .config('spark.debug.maxToStringFields', 2000) \
        .getOrCreate()
    sqlContext = SQLContext(sc)
    n_hydrated_tweets = 2

    # schema for the hydrated tweets dataframe
    schema = StructType([
        StructField('full_text', StringType(), True),
        StructField('id', StringType(), True),
        StructField('created_at', StringType(), True)
    ])

    # creation of an empty rdd that will be used to store the hydrated tweets
    hydrated_tweets_df = spark.createDataFrame(
        spark.sparkContext.emptyRDD(), schema)

    for i in range(1, n_hydrated_tweets+1):
        if i < 10:
            ind = '0' + str(i)
        else:
            ind = str(i)
        source_path = r"C:\Users\Davide\id_tweets\hydrated_tweets_" + ind + '.jsonl'
        df = sqlContext.read.json(source_path)
        df_small = df.select('full_text', 'id_str', 'created_at')
        # print(df_small.count())
        hydrated_tweets_df = hydrated_tweets_df.union(df_small)

    schema = StructType([
        StructField('full_text', StringType(), True),
        StructField('id', StringType(), True),
        StructField('created_at', StringType(), True)
    ])
    hydrated_tweets_df = spark.createDataFrame(
        spark.sparkContext.emptyRDD(), schema)

    for i in range(1, n_hydrated_tweets+1):
        if i < 10:
            ind = '0' + str(i)
        else:
            ind = str(i)
        source_path = r"C:\Users\Davide\id_tweets\hydrated_tweets_" + ind + '.jsonl'
        df = sqlContext.read.json(source_path)
        df_small = df.select('full_text', 'id_str', 'created_at')
        # print(df_small.count())
        hydrated_tweets_df = hydrated_tweets_df.union(df_small)

    schema_2 = StructType([
        StructField('tweet_id', StringType(), True),
        StructField('sentiment', FloatType(), True)
    ])

    tweets_sentiment_df = spark.createDataFrame(
        spark.sparkContext.emptyRDD(), schema_2)

    for i in range(1, n_hydrated_tweets+1):
        if i < 10:
            ind = '0' + str(i)
        else:
            ind = str(i)
        path = r'C:\Users\Davide\id_tweets\csv_tweets\corona_tweets_' + ind + '.csv'
        df_small = sqlContext.read.format('com.databricks.spark.csv') \
            .options(header='false', inferschema='false', quote='"', delimiter=',').schema(schema_2) \
            .load(path)
        tweets_sentiment_df = tweets_sentiment_df.union(df_small)

    joined_df = hydrated_tweets_df.join(
        tweets_sentiment_df, hydrated_tweets_df['id'] == tweets_sentiment_df['tweet_id'], 'inner')

    # We drop the columns we don't need in our joined dataset
    drop_columns = ['id', 'tweet_id']

    data_df = joined_df.select(
        [column for column in joined_df.columns if column not in drop_columns])
    data_df.show(5)

    # registering the UDF
    discretize_sentiment_udf = spark.udf.register(
        "discretize_sentiment", discretize_sentiment, IntegerType())

    data_df = data_df.withColumn(
        'label', discretize_sentiment_udf(col('sentiment')))

    data_df = regex_data_cleaning(data_df)
    return data_df


def regex_data_cleaning(data):
    patterns_to_replace = {r'@\w*': '',
                           r'(\s?:X|:|;|=)(?:-)?(?:\)+|\(|O|D|P|S|\\|\/\s){1,}': '',
                           r'(\.+)|(\_)|(\«)|(\»)|(\;)|(\:)|(\!)|(\?)|(\,)|(\")|(\“)|(\”)|(\’)|(\|)|(\()|(\))|(\[)|(\])|(\%)|(\$)|(\>)|(\<)|(\{)|(\})': '',
                           r'#': '',
                           r'\n': ' ',
                           r'(<br\s/><br\s/?)|(-)|(/)|(\')|(:).': '',
                           r'\b[0-9]+\b': '',
                           r'(https?:\/\/)(\s)*(www\.)?(\s)*((\w|\s)+\.)*([\w\-\s]+\/)*([\w\-]+)((\?)?[\w\s]*=\s*[\w\%&]*)*': ''}
    for key, val in patterns_to_replace.items():
        data = data.withColumn(
            'full_text', regexp_replace(col('full_text'), key, val))
    return data

# Function to discretize the 'sentiment' column, which is a float

# This function will be used as ad UDF to discretize the 'sentiment' column, which is originally a float, into an integer
# ranging from 0 to 3


def discretize_sentiment(sentiment) -> int:
    if(sentiment < -0.5):
        return 0
    if(sentiment >= -0.5 and sentiment <= 0):
        return 1
    if(sentiment > 0 and sentiment <= 0.5):
        return 2
    if(sentiment > 0.5):
        return 3
