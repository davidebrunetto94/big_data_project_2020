# Trend analysis and Multi-Class TextClassification on a dataset of tweets regarding Covid-19 with PySpark
This project uses a [Kaggle dataset](https://www.kaggle.com/varisha25/ieee-covid19-tweets-dataset) which contains the ids of tweets regarding the current covid-19 pandemic and their sentiment and, using Spark, analyzes them to understand how the phenomenon has changes over the course of time, for example showing the trend of the volume of tweets, or showing the trend of the "sentiment" value.
As per the Twitter Developer Policy, the dataset doesn't provide the tweet's text, but only provides the Tweet IDs, we thus had to "hydrate" the tweets using [Twarc](https://github.com/DocNow/twarc), a command line tool the using the Twitter Developer API, allowed us to gather the complete tweets from their IDs.
The data obtained from the hydration process was then used to train a machine learning algorithm, specifically a logistic regression model, to predict the sentiment of the tweet based on its text, with a value ranging from 0, which means a strong negative sentiment, to 4, which means a strong positive sentiment. To do so, the "sentiment" field, which was originally a continuous value ranging from -1 to 1, was discretized into a value ranging from 0 to 4.
Finally, we tested the project on various number of instances to show the perfomance improvement brought by a greater number of computation nodes.

1. [Structure](#Structure)
2. [How to run](#How-to-run)

## Structure
* proj: contains the application script. It is composed of 6 main modules:
    * **data_preprocessing.py**, which is a small utility script that takes in input the starting dataset, composed of a .csv file that has two fields, the tweet ID and sentiment, and creates a .txt file only containing the first field. This .txt file will be used for the tweet hydration;
    * **tweet_hydration.sh**, which is a bash script that takes in input the .txt file created by **data_preprocessing.py** and uses Twarc to hydrate the tweets;
    * **jsonl_to_csv.py**, which is a module that takes in input the jsonl files returned from **tweet_hydration.sh** and creates a csv file for each one of them, containing only the fields that we need for our analysis;

   Since these two last operations are very time-consuming, the already hydrated files can be downloaded from [here](https://drive.google.com/file/d/1pM_Us5wodfXn0FEUMXOf15G3k1dUR7Bo/view?usp=sharing)
    * **data_manipulation.py**, this module is composed of all the functions that take in input 'raw' tweets data, and manipulate it to make it better suited for the machine learning process. This includes functions that gather the data from the csv files and generates Pyspark dataframes using the Pyspark sql module, a function to discretize the sentiment of the tweets, a function that uses regular expressions to clean the text of the tweets, a function to create a stratified sampling of the data, and so on...;
    * **machine_learning.py**, this module handles all the machine learning related tasks. It takes in input the clean data and then, creats a feature vector using tf-idf, this vector is then used to train a model to predict the sentiment of the tweets. A number of differet models were tested, in the end our choice fell on a linear SVM as it gave the best overall metrics, achieving a precision of around 90%. The experiments with the other models were left in the code, commented out;
    * **trend_graphs.py**, this module handles the trend graphs. The module takes in input a dataframe called "sentiment_df", which contains the average sentiment of the tweets grouped by day, and a second dataframe called "count_df" which contains the count of the tweets grouped by day. This second dataframe was created using the dehydrated tweets id, because of the fact that the volume of the hydrated tweets is smaller than the counts of tweet IDs since some tweets were deleted afterwards.

* terraform-aws-instance(educate): contains the scripts needed to create the environment on AWS educate account

* terraform-aws-instance(classic): contains the scripts needed to create the environment on AWS classic account

## How to run
Copy the dataset files in to ```tweet_data``` directory in the master node.
I suggest using FileZilla to perform this operation.
If you need a simple guide to do this, you can find it [here](https://angus.readthedocs.io/en/2014/amazon/transfer-files-between-instance.html)

From AWS EC2 consolle, activate all instances you need.

Login into master instance:
```
$ssh -i chiave_aws.pem ubuntu@<-Master-dns-address->
```

Run HDFS:
```
$HADOOPHOME/sbin/start-dfs.sh
$HADOOPHOME/sbin/start-yarn.sh
$HADOOPHOME/sbin/mr-jobhistory-daemon.sh start historyserver
```

Copy the dataset into HDFS disk:
```
hdfs dfs -mkdir /home
hdfs dfs -mkdir /home/ubuntu
hdfs dfs -put tweet_data /home/ubuntu/tweet_data
```

Run Spark:
```
$SPARKHOME/sbin/start-master.sh
$SPARKHOME/sbin/start-slaves.sh spark://s01:7077
```


To run the machine learning module of the project, use this command:
ATTENTION: replace the number of cores and memory based on the type of instances you have chosen to use.

```
/opt/spark-3.0.2-bin-hadoop2.7/bin/spark-submit --masterspark://s01:7077 --executor-cores 4 --executor-memory 14gmachinelearning.py
```
To run the trend analysis module of the project, use this command:
```
/opt/spark-3.0.2-bin-hadoop2.7/bin/spark-submit --masterspark://s01:7077 --executor-cores 4 --executor-memory 14gtrendgraphs.py
```
