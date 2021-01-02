import pandas as pd
from twarc import Twarc
from secrets import CONS_KEY, CONS_SECRET, ACC_SECRET, ACC_TOKEN

id_path = r'..\id_tweets_head30.txt'
column_names = ["created_at", "full_text", "id_str"]
df = pd.DataFrame(columns=column_names)

# Twarc initialization
t = Twarc(CONS_KEY, CONS_SECRET, ACC_TOKEN, ACC_SECRET)
for tweet in t.hydrate(open(id_path)):
    new_row = {'created_at': tweet['created_at'],
               'full_text': tweet['full_text'], 'id_str': tweet['id_str']}
    # append row to the dataframe
    df = df.append(new_row, ignore_index=True)
    # print(df)

df.to_csv(r"..\hydrated_tweets_short.csv", sep='\t', index=False)
