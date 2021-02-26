# Trend analysis and Multi-Class TextClassification on a dataset of tweets regarding Covid-19 with PySpark
This project uses a [Kaggle dataset](https://www.kaggle.com/varisha25/ieee-covid19-tweets-dataset) which contains the ids of tweets regarding the current covid-19 pandemic and their sentiment and, using Spark, analyzes them to understand how the phenomenon has changes over the course of time, for example showing the trend of the volume of tweets, or showing the trend of the "sentiment" value.
As per the Twitter Developer Policy, the dataset doesn't provide the tweet's text, but only provides the Tweet IDs, we thus had to "hydrate" the tweets using [Twarc](https://github.com/DocNow/twarc), a command line tool the using the Twitter Developer API, allowed us to gather the complete tweets from their IDs.
The data obtained from the hydration process was then used to train a machine learning algorithm, specifically a logistic regression model, to predict the sentiment of the tweet based on its text, with a value ranging from 0, which means a strong negative sentiment, to 4, which means a strong positive sentiment. To do so, the "sentiment" field, which was originally a continuous value ranging from -1 to 1, was discretized into a value ranging from 0 to 4.
Finally, we tested the project on various number of instances to show the perfomance improvement brought by a greater number of computation nodes.

1. [Structure](#Structure)
2. [How to run](#How To Run)

## Structure
* proj: contains the application script. It is composed of x main modules:
    * **data_preprocessing.py**, which is a small utility script that takes in input the starting dataset, composed of a .csv file that has two fields, the tweet ID and sentiment, and creates a .txt file only containing the first field. This .txt file will be used for the tweet hydration;
    * **tweet_hydration.sh**, which is a bash script that takes in input the .txt file created by **data_preprocessing.py** and uses Twarc to hydrate the tweets;
    * **jsonl_to_csv.py**, which is a module that takes in input the jsonl files returned from **tweet_hydration.py** and creates a csv file for each one of them, containing only the fields that we need for our analysis;
    * **data_manipulation.py**, this module is composed of all the functions that take in input 'raw' tweets data, and manipulate it to make it better suited for the machine learning process. This includes functions that gather the data from the csv files and generates Pyspark dataframes using the Pyspark sql module, a function to discretize the sentiment of the tweets, a function that uses regular expressions to clean the text of the tweets, a function to create a stratified sampling of the data, and so on...;
    * **machine_learning.py**, this module handles all the machine learning related tasks. It takes in input the clean data and then, using logistic regression, creates a model to predict the sentiment of the tweets. This model achieves a precision of xx.y%;
    * **trend_graphs.py**, this module handles the trend graphs. The module takes in input a dataframe called "sentiment_df", which contains the average sentiment of the tweets grouped by day, and a second dataframe called "count_df" which contains the count of the tweets grouped by day. This second dataframe was created using the dehydrated tweets id, because of the fact that the volume of the hydrated tweets is smaller than the counts of tweet IDs since some tweets were deleted afterwards.
* bigdata-terraform-aws-instance: contiene gli script necessari alla creazione dell'ambiente su AWS

## HowToRun
To run the machine learning module of the project, use this command:
```
/opt/spark/bin/spark-submit ./proj/machine_learning.py
```
To run the trend analysis module of the project, use this command:
```
/opt/spark/bin/spark-submit ./proj/trend_graphs.py
```
