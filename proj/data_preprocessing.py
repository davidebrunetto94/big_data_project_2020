import pandas as pd

# the number of files our dataset has
dataset_dim = 86

for i in range(1, dataset_dim+1):
    if i < 10:
        ind = '0' + str(i)
    else:
        ind = str(i)
    path_tweets = r'C:\Users\Davide\Desktop\corona_tweets\corona_tweets_' + ind + '.csv'
    dataframe = pd.read_csv(path_tweets, header=None)
    dataframe = dataframe[0]
    path_ids = r'C:\Users\Davide\Desktop\corona_tweets\id_tweets_' + ind + '.txt'
    dataframe.to_csv(path_ids, index=False, header=None)
