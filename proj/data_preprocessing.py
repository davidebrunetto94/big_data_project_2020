from data_manipulation import get_spark_sql_context
import os
import time
import re

start_time = time.time()
dataset_dim = 86
spark, sqlContext = get_spark_sql_context()
for i in range(1, dataset_dim+1):
    if i < 10:
        ind = '0' + str(i)
    else:
        ind = str(i)
    path_tweets = r'C:\Users\Davide\id_tweets\csv_tweets\corona_tweets_' + ind + '.csv'
    df_small = sqlContext.read.format('csv').option(
        'header', False).load(path_tweets).select('_c0')
    path_ids = r'C:\Users\Davide\Desktop\pro\df_tweets' + ind + '.txt'
    df_small.coalesce(1).write.format("text").option(
        "header", "false").mode("append").save(path_ids)
    for filename in os.listdir(path_ids):
        if re.match("part-.+[.txt]$", filename):
            print("match")
            new_path = r"C:\Users\Davide\Desktop\pro\txt_tweets"
            new_name = r"txt_tweets_" + ind + ".txt"
            os.rename(os.path.join(path_ids, filename),
                      os.path.join(new_path, new_name))
print("--- %s seconds ---" % (time.time() - start_time))
