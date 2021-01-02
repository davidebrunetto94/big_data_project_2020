from data_manipulation import get_timestamped_tweet_sentiment_df
from pyspark.ml.evaluation import MulticlassClassificationEvaluator
from pyspark.ml.feature import OneHotEncoder, StringIndexer, VectorAssembler
from pyspark.ml import Pipeline
from pyspark.ml.feature import RegexTokenizer, StopWordsRemover, CountVectorizer
from pyspark.ml.classification import LogisticRegression
import nltk
from nltk.corpus import stopwords

data_df = get_timestamped_tweet_sentiment_df(1)
