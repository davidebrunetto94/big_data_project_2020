from pyspark.ml.feature import OneHotEncoder, StringIndexer, VectorAssembler
from pyspark.ml import Pipeline
from pyspark.ml.feature import RegexTokenizer, StopWordsRemover, CountVectorizer
from pyspark.ml.classification import LogisticRegression
import nltk
from nltk.corpus import stopwords
from data_manipulation import get_clean_data

data_df = get_clean_data()
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
