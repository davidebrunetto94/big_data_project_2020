import datetime

import matplotlib.dates as mdates
import matplotlib.pyplot as plt

from data_manipulation import get_avg_tweet_sentiment_df, get_tweet_count_df

# Questo modulo si occupa di generare i grafici relativi al sentimento e al volume dei tweet
# E' necessaria la libreria matplotlib e prende i dati dal modulo data_manipulation
# che contiene il sentimento medio il count dei tweet giornalieri


# SENTIMENTO MEDIO

sentiment_df = get_avg_tweet_sentiment_df(30)
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


# VOLUME DEI TWEET

count_df = get_tweet_count_df()
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
