import nltk
import time
from nltk.corpus import stopwords
from pyspark.ml import Pipeline
from pyspark.ml.classification import (LinearSVC, LogisticRegression,
                                       NaiveBayes, OneVsRest)
from pyspark.ml.evaluation import MulticlassClassificationEvaluator
from pyspark.ml.feature import (IDF, CountVectorizer, HashingTF,
                                RegexTokenizer, StopWordsRemover)
from pyspark.mllib.classification import SVMModel, SVMWithSGD
from pyspark.mllib.evaluation import MulticlassMetrics
from pyspark.mllib.util import MLUtils

from data_manipulation import get_clean_ml_dataset

# Start stopwatch for calculating the running time
start_time = time.time()
print("Start...")

# We get the clean dataset for machine learning
data_df = get_clean_ml_dataset()

print("data_df loaded")

# regular expression tokenizer
regexTokenizer = RegexTokenizer(
    inputCol="full_text", outputCol="words", pattern="\\W")

# Download of english stopwords
nltk.download('stopwords')
# we add some tweet specific stopwords, such as RT, fav, FAV
english_stopwords = stopwords.words('english') + ["RT", "rt", "FAV", "fav"]
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

# We split the dataset into test set and training set
(trainingData, testData) = dataset.randomSplit([0.7, 0.3], seed=0)
trainingData.show(5)

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
