from pyspark.ml.evaluation import MulticlassClassificationEvaluator
from pyspark.ml.feature import OneHotEncoder, StringIndexer, VectorAssembler
from pyspark.ml import Pipeline
from pyspark.ml.feature import RegexTokenizer, StopWordsRemover, CountVectorizer
from pyspark.ml.classification import LogisticRegression
import nltk
from nltk.corpus import stopwords
from data_manipulation import get_clean_ml_dataset

data_df = get_clean_ml_dataset()

class_count = data_df.groupBy(
    "label").count()
print('--------------------CLASS COUNT -------------------------------')
class_count.show(10)
# regular expression tokenizer
regexTokenizer = RegexTokenizer(
    inputCol="full_text", outputCol="words", pattern="\\W")

# Download of english stopwords
nltk.download('stopwords')
# we add some tweet specific stopwords, such as RT, fav, FAV
english_stopwords = stopwords.words('english') + ["RT", "rt", "FAV", "fav"]
stopwordsRemover = StopWordsRemover(
    inputCol="words", outputCol="filtered").setStopWords(english_stopwords)

# bag of words count
countVectors = CountVectorizer(
    inputCol="filtered", outputCol="features", vocabSize=10000, minDF=5)


# we create a pipeline for the ML process
pipeline = Pipeline(stages=[regexTokenizer, stopwordsRemover, countVectors])
# Fit the pipeline to training documents.
pipelineFit = pipeline.fit(data_df)
dataset = pipelineFit.transform(data_df)
dataset.show(5)

(trainingData, testData) = dataset.randomSplit([0.7, 0.3], seed=0)
print("Training Dataset Count: " + str(trainingData.count()))
print("Test Dataset Count: " + str(testData.count()))

lr = LogisticRegression(maxIter=20, regParam=0.3, elasticNetParam=0)
lrModel = lr.fit(trainingData)
predictions = lrModel.transform(testData)
# predictions.select("full_text", "sentiment", "probability", "label", "prediction", "filtered") \
#     .show(n=10, truncate=30)

evaluator = MulticlassClassificationEvaluator(predictionCol="prediction")
print("The accuracy of the evaluator model is " +
      str(evaluator.evaluate(predictions)))

print('F1-Score ', evaluator.evaluate(predictions,
                                      {evaluator.metricName: 'f1'}))
print('Precision ', evaluator.evaluate(predictions,
                                       {evaluator.metricName:                    'weightedPrecision'}))
print('Recall ', evaluator.evaluate(predictions,
                                    {evaluator.metricName: 'weightedRecall'}))
print('Accuracy ', evaluator.evaluate(predictions,
                                      {evaluator.metricName: 'accuracy'}))
