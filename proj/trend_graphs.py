import datetime
import time
import matplotlib.dates as mdates
import matplotlib.pyplot as plt

from data_manipulation import get_avg_tweet_sentiment_df, get_tweet_count_df
from get_spark_context import get_spark_sql_context

spark, sqlContext = get_spark_sql_context()

# This module generates the graphs for the sentiment and tweet volume.
# It uses the matplotlib library and get its data from data_manipulation

# Parameter for the number of nodes used in the cluster
n_nodes = 4
# Parameter for the number of cores of a node
n_cores = 4
# Parameter for the number of dataset to use
n_dataset = 30



n_partitions = n_cores*n_nodes
# Start stopwatch for calculating the running time
start_time = time.time()
print("Start...")

# Sentiment graph
sentiment_df = get_avg_tweet_sentiment_df(n_dataset, n_partitions, spark, sqlContext, False)
x = sentiment_df.select('timestamp').rdd.map(
    lambda x: datetime.datetime.strftime(x[0], "%d/%m/%Y")).collect()
y = sentiment_df.select('avg(sentiment)').rdd.map(lambda x: x[0]).collect()
#ax = plt.gca()
f1 = plt.figure()
plt.xticks(rotation=90, fontsize=7)
plt.xlabel('dates', fontsize=5)
plt.plot(x, y)
plt.savefig('sentiment_trend_graph.png', bbox_inches="tight")
f1.clear()
plt.close(f1)


# Tweet volume graph
count_df = get_tweet_count_df(n_dataset, spark, sqlContext)
x = count_df.select('timestamp').rdd.map(
    lambda x: datetime.datetime.strftime(x[0], "%d/%m/%Y")).collect()
y = count_df.select('count').rdd.map(lambda x: x[0]).collect()
#ax2 = plt.gca()
f2 = plt.figure()
plt.xticks(rotation=90, fontsize=7)
plt.xlabel('dates', fontsize=5)
plt.plot(x, y)
plt.savefig('volume_trend_graph.png', bbox_inches="tight")
f2.clear()
plt.close(f2)

print("--- Execution time: %s seconds ---" % (time.time() - start_time))
