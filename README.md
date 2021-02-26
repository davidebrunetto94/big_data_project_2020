# Trend analysis e Multi-Class TextClassification su dataset di tweetriguardanti il Covid-19 con Pyspark

This project consists in collecting all the tweets related to the "Covid-19" topic of 2020 (or part of them) and analyzing how the phenomenon has changed over time, for example showing the growth in the volume of tweets over time, or showing how the trend of the "sentiment" field of tweets varies during the various phases of the pandemic.
The tweet data was used to train a machine learning model (likely an SVM) to predict the sentiment of the tweet text in a binary fashion as positive or negative. To do this, the sentiment, which in the dataset is a continuous value between the value -1 and the value 1, has been converted into a binary value.
Finally, tests were performed on data processing starting from two instances and gradually increased to five by measuring the performance that will then be compared.

1. [Goals](#Goals)
2. [Project structure](#Project-structure)

## Goals
This project uses a Kaggle dataset, which contains the IDs of the tweets regarding the current covid-19 pandemic and their sentiment, for two purposes:
- Analysis, understand how the phenomenon has changed over time, for example by showing the trend in the volume of tweets, or by showing the trend in the value of the "sentiment" field.
- Classification and prediction, training machine learning models to predict if a tweet expresses a positive or negative feeling, starting from the text of this.
These goals were achieved using PySpark and its libraries.

## Project structure
* proj: contains application scripts
* bigdata-terraform-aws-instance: contains the scripts needed to create the environment on AWS
