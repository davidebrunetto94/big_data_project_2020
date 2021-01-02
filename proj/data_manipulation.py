from pyspark import SparkContext, SparkConf
from pyspark.sql import SparkSession
from pyspark.sql.types import StructType, StringType, FloatType, StructField, IntegerType, LongType
from pyspark.sql import SQLContext
from pyspark.sql.functions import regexp_replace, col, asc
import pyspark
import findspark
findspark.init()
findspark.find()


def get_timestamped_tweet_sentiment_df(n):
    import time
    spark, _ = get_spark_sql_context()
    tweets_sentiment_df = get_tweets_sentiment_df(n)
    tweets_sentiment_df = tweets_sentiment_df.withColumn(
        "tweet_id", col('tweet_id').cast(LongType()))

    timestamp_from_id_udf = spark.udf.register(
        "timestamp_from_id", timestamp_from_id)

    timestamped_tweets_sentiment_df = tweets_sentiment_df.withColumn(
        'timestamp', timestamp_from_id_udf(col('tweet_id')))
    timestamped_tweets_sentiment_df.show(5)
    return timestamped_tweets_sentiment_df


def timestamp_from_id(id):
    import datetime as dt
    shifted_id = id >> 22  # applying right shift operator to the tweet ID
    timestamp = shifted_id + 1288834974657
    file_time = dt.datetime.fromtimestamp(timestamp/1000)
    return file_time.strftime("%d %m %Y")


def get_spark_sql_context():
    conf = pyspark.SparkConf().setAppName('appName').setMaster('local')
    sc = pyspark.SparkContext.getOrCreate(conf=conf)
    spark = SparkSession \
        .builder \
        .master('local') \
        .appName('Notebook') \
        .config('spark.sql.debug.maxToStringFields', 2000) \
        .config('spark.debug.maxToStringFields', 2000) \
        .getOrCreate()
    sqlContext = SQLContext(sc)
    return [spark, sqlContext]


def get_hydrated_tweets_dataset(n):
    spark, sqlContext = get_spark_sql_context()
    schema = StructType([
        StructField('full_text', StringType(), True),
        StructField('id_str', StringType(), True),
        StructField('created_at', StringType(), True)
    ])

    # creation of an empty rdd that will be used to store the hydrated tweets
    hydrated_tweets_df = spark.createDataFrame(
        spark.sparkContext.emptyRDD(), schema)

    for i in range(1, n+1):
        if i < 10:
            ind = '0' + str(i)
        else:
            ind = str(i)
        source_path = r'C:\Users\Davide\id_tweets\hydrated_tweets_csv\hydrated_tweets_' + ind + '.csv'
        df_small = sqlContext.read.format('com.databricks.spark.csv') \
            .options(header='true', inferschema='false', quote='"', delimiter='\t', multiLine='true', schema=schema) \
            .load(source_path)
        # print(df_small.count())
        hydrated_tweets_df = hydrated_tweets_df.union(df_small)

    print("-----------------------------HYDRATED TWEETS ---------------------------------")
    hydrated_tweets_df.show(20)
    return hydrated_tweets_df


def get_tweets_sentiment_df(n):
    spark, sqlContext = get_spark_sql_context()
    schema_2 = StructType([
        StructField('tweet_id', StringType(), True),
        StructField('sentiment', FloatType(), True)
    ])

    tweets_sentiment_df = spark.createDataFrame(
        spark.sparkContext.emptyRDD(), schema_2)

    for i in range(1, n+1):
        if i < 10:
            ind = '0' + str(i)
        else:
            ind = str(i)
        path = r'C:\Users\Davide\id_tweets\csv_tweets\corona_tweets_' + ind + '.csv'
        df_small = sqlContext.read.format('com.databricks.spark.csv') \
            .options(header='false', inferschema='false', quote='"', delimiter=',').schema(schema_2) \
            .load(path)
        tweets_sentiment_df = tweets_sentiment_df.union(df_small)

    print("----------------------------- TWEETS SENTIMENT ---------------------------------")
    tweets_sentiment_df.show(5)
    return tweets_sentiment_df


def get_clean_ml_dataset():
    spark, _ = get_spark_sql_context()
    n_datasets = 10  # the number of datasets we want to use

    hydrated_tweets_df = get_hydrated_tweets_dataset(n_datasets)
    tweets_sentiment_df = get_tweets_sentiment_df(n_datasets)
    joined_df = hydrated_tweets_df.join(
        tweets_sentiment_df, hydrated_tweets_df['id_str'] == tweets_sentiment_df['tweet_id'], 'inner')
    print("----------------------------- JOINED DF ---------------------------------")
    joined_df.show(5)

    # We drop the columns we don't need in our joined dataset
    drop_columns = ['id_str', 'tweet_id']
    data_df = joined_df.select(
        [column for column in joined_df.columns if column not in drop_columns])
    print("----------------------------- DATA DF ---------------------------------")
    data_df.show(5)

    # registering the UDF
    discretize_sentiment_udf = spark.udf.register(
        "discretize_sentiment", discretize_sentiment, IntegerType())

    # creation of a column 'label' with a discrete value from 0 to 3 for the sentiment score
    data_df = data_df.withColumn(
        'label', discretize_sentiment_udf(col('sentiment')))

    data_df = regex_data_cleaning(data_df)
    return stratified_sampling(100000, data_df)

# Function to 'clean' the dataset using regular expressions


def regex_data_cleaning(data):
    # a dictionary that has as keys the patterns to replace and as values what we want to replace those patterns with
    patterns_to_replace = {r'@\w*': '',
                           r'(https?:\/\/)(\s)*(www\.)?(\s)*((\w|\s)+\.)*([\w\-\s]+\/)*([\w\-]+)((\?)?[\w\s]*=\s*[\w\%&]*)*': '',
                           r'(\s?:X|:|;|=)(?:-)?(?:\)+|\(|O|D|P|S|\\|\/\s){1,}': '',
                           r'(\.+)|(\_)|(\«)|(\»)|(\;)|(\:)|(\!)|(\?)|(\,)|(\")|(\“)|(\”)|(\’)|(\|)|(\()|(\))|(\[)|(\])|(\%)|(\$)|(\>)|(\<)|(\{)|(\})': '',
                           r'#': '',
                           r'\n': ' ',
                           r'(<br\s/><br\s/?)|(-)|(/)|(\')|(:).': '',
                           r'\b[0-9]+\b': ''}
    for key, val in patterns_to_replace.items():
        data = data.withColumn(
            'full_text', regexp_replace(col('full_text'), key, val))
    return data


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


# This function returns a stratified sampling of a dataset with the size of around dim_sample. If there are not enough elements from the least
# popular class to make the sample with dim_sample, the size of the sample returned will be 4 times the number of elements from the least popular class
def stratified_sampling(dim_sample, dataset):
    # This should be dim_sample / num_classes computed as the distinct values for the column "label", but we hardcode 4 to save time
    num_element_per_class = dim_sample / 4

    class_count_asc = dataset.groupBy(
        "label").count().sort(asc('count'))

    n_least_pop_class = class_count_asc.first()['count']

    # This is to avoid having fractions higher than 1
    if num_element_per_class > n_least_pop_class:
        num_element_per_class = n_least_pop_class

    # checking how the class are distributed
    classes_distribution = class_count_asc.withColumn('percentage', num_element_per_class / col('count')) \
        .sort(asc('percentage')).select('label', 'percentage').rdd.collectAsMap()

    print(classes_distribution)

    return dataset.sampleBy("label", fractions=classes_distribution, seed=0)
