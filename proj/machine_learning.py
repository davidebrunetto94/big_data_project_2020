import time

import findspark
import pyspark
from nltk.corpus import stopwords
from pyspark import SparkConf, SparkContext
from pyspark.ml import Pipeline
from pyspark.ml.classification import (LinearSVC, LogisticRegression,
                                       NaiveBayes, OneVsRest)
from pyspark.ml.evaluation import MulticlassClassificationEvaluator
from pyspark.ml.feature import (IDF, CountVectorizer, HashingTF,
                                RegexTokenizer, StopWordsRemover)
from pyspark.mllib.classification import SVMModel, SVMWithSGD
from pyspark.mllib.evaluation import MulticlassMetrics
from pyspark.mllib.util import MLUtils
from pyspark.sql import SparkSession, SQLContext

from data_manipulation import get_clean_ml_dataset
from get_spark_context import get_spark_sql_context

findspark.init()
findspark.find()


# Start stopwatch for calculating the running time
start_time = time.time()
print("Start...")
spark, sqlContext = get_spark_sql_context()

# Parameter for the number of nodes in the cluster
n_nodes = 4
# Parameter for the number of cores of a node
n_cores = 4
# Parameter for the number of dataset in the cluster
n_dataset = 4


n_partitions = n_cores*n_nodes
# We get the clean dataset for machine learning
data_df = get_clean_ml_dataset(n_dataset, n_partitions, spark, sqlContext)
data_df.persist()
print("data_df loaded")

# regular expression tokenizer
regexTokenizer = RegexTokenizer(
    inputCol="full_text", outputCol="words", pattern="\\W")

#We use a precompiled list of stopwords to avoid downloading them each time, and then add some twitter specific ones
english_stopwords = ['i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves', 'you',
    "you're", "you've", "you'll", "you'd", 'your', 'yours', 'yourself', 'yourselves', 
    'he', 'him', 'his', 'himself', 'she', "she's", 'her', 'hers', 'herself', 'it', "it's",
    'its', 'itself', 'they', 'them', 'their', 'theirs', 'themselves', 'what', 'which', 
    'who', 'whom', 'this', 'that', "that'll", 'these', 'those', 'am', 'is', 'are', 'was',
    'were', 'be', 'been', 'being', 'have', 'has', 'had', 'having', 'do', 'does', 'did',
    'doing', 'a', 'an', 'the', 'and', 'but', 'if', 'or', 'because', 'as', 'until', 'while',
    'of', 'at', 'by', 'for', 'with', 'about', 'against', 'between', 'into', 'through',
    'during', 'before', 'after', 'above', 'below', 'to', 'from', 'up', 'down', 'in',
    'out', 'on', 'off', 'over', 'under', 'again', 'further', 'then', 'once', 'here',
    'there', 'when', 'where', 'why', 'how', 'all', 'any', 'both', 'each', 'few',
    'more', 'most', 'other', 'some', 'such', 'no', 'nor', 'not', 'only', 'own', 
    'same', 'so', 'than', 'too', 'very', 's', 't', 'can', 'will', 'just', 'don',
    "don't", 'should', "should've", 'now', 'd', 'll', 'm', 'o', 're', 've', 'y',
    'ain', 'aren', "aren't", 'couldn', "couldn't", 'didn', "didn't", 'doesn',
    "doesn't", 'hadn', "hadn't", 'hasn', "hasn't", 'haven', "haven't", 'isn',
    "isn't", 'ma', 'mightn', "mightn't", 'mustn', "mustn't", 'needn', "needn't",
    'shan', "shan't", 'shouldn', "shouldn't", 'wasn', "wasn't", 'weren', "weren't",
    'won', "won't", 'wouldn', "wouldn't", "RT", "rt", "FAV", "fav"]

stopwordsRemover = StopWordsRemover(
    inputCol="words", outputCol="filtered").setStopWords(english_stopwords)
# This part shows two different methods for the creation of the vector of features that will be used to
# classify the tweets, the first is a simple count vector, while the second is a tf-idf vector.
# in the end, we chose the second one as it gave the best accuracy.

# bag of words count
# countVectors = CountVectorizer(
#     inputCol="filtered", outputCol="features", vocabSize=10000, minDF=5)

# tf-idf vector
hashingTF = HashingTF(inputCol="filtered",
                      outputCol="rawFeatures", numFeatures=10000)
idf = IDF(inputCol="rawFeatures", outputCol="features", minDocFreq=5)

# creation of the pipeline
pipeline = Pipeline(stages=[regexTokenizer, stopwordsRemover, hashingTF, idf])
# Fit of the pipeline to the training documents
pipelineFit = pipeline.fit(data_df)
dataset = pipelineFit.transform(data_df)

data_df.unpersist()
# We split the dataset into test set and training set
(trainingData, testData) = dataset.randomSplit([0.7, 0.3], seed=0)
trainingData.persist()
testData.persist()

# Caching of the training and test data
trainingData.persist()
testData.persist()
# trainingData.show(5)

# print("Training Dataset Count: " + str(trainingData.count()))
# print("Test Dataset Count: " + str(testData.count()))


# This part shows two different ML models, the first one is a logistic regression model, the second one is a Naive Bayes
# model. We chose the second model because it gave the best results.

# # logistic regression model
# lr = LogisticRegression(maxIter=20, regParam=0.3, elasticNetParam=0)
# lrModel = lr.fit(trainingData)
# predictions = lrModel.transform(testData)
# predictions.select("full_text", "sentiment", "probability", "label", "prediction", "filtered") \
#     .show(n=10, truncate=30)
# lr = LogisticRegression(maxIter=10, regParam=0.3, elasticNetParam=0)
# lrModel = lr.fit(trainingData)
# predictions = lrModel.transform(testData)

# # Naive Bayes model
# nb = NaiveBayes(smoothing=2)
# model = nb.fit(trainingData)
# predictions = model.transform(testData)#.rdd.map(lambda x: (float(x[3]), x[10]))


# This part shows the third classifier, a linear SVC of type one vs rest.
# Definition of the binary classifier
lsvc = LinearSVC(maxIter=10, regParam=0.1).setTol(0.1)
# Definition of the OVR classifier
ovr = OneVsRest(classifier=lsvc)
# train the multiclass model.
ovrModel = ovr.fit(trainingData)
# make the predictions on the test data
predictions = ovrModel.transform(testData)

# #This part evaluates the performance of the model. We used precision, recall and F1-Measure as metrics.
# obtain evaluator.
evaluator_acc = MulticlassClassificationEvaluator(metricName="accuracy")
evaluator_prec = MulticlassClassificationEvaluator(
    metricName="weightedPrecision")
evaluator_recall = MulticlassClassificationEvaluator(
    metricName="weightedRecall")
evaluator_f1Score = MulticlassClassificationEvaluator(metricName="f1")

accuracy = evaluator_acc.evaluate(predictions)
precision = evaluator_prec.evaluate(predictions)
recall = evaluator_recall.evaluate(predictions)
f1Score = evaluator_f1Score.evaluate(predictions)
print("Accuracy = %s" % accuracy)
print("Precision = %s" % precision)
print("Recall = %s" % recall)
print("F1 Score = %s" % f1Score)
print("--- Execution time: %s seconds ---" % (time.time() - start_time))
