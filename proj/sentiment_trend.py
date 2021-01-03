from data_manipulation import get_avg_tweet_sentiment_df
from pyspark.ml.evaluation import MulticlassClassificationEvaluator
from pyspark.ml.feature import OneHotEncoder, StringIndexer, VectorAssembler
from pyspark.ml import Pipeline
from pyspark.ml.feature import RegexTokenizer, StopWordsRemover, CountVectorizer
from pyspark.ml.classification import LogisticRegression
import nltk
from nltk.corpus import stopwords
import matplotlib.pyplot as plt
import datetime
import matplotlib.dates as mdates

data_df = get_avg_tweet_sentiment_df(3)
x = data_df.select('timestamp').rdd.map(
    lambda x: datetime.datetime.strftime(x[0], "%d/%m/%Y")).collect()
y = data_df.select('avg(sentiment)').rdd.map(lambda x: x[0]).collect()

ax = plt.gca()
plt.xticks(rotation=90, fontsize=7)
plt.xlabel('dates', fontsize=5)
plt.plot(x, y)
plt.savefig('sentiment_trend_graph.png', bbox_inches="tight")
