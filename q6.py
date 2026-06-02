import os
import pandas as pd
from q1 import process_mati_data

input_file = "data/mati_q1_relevant.csv"
if os.path.exists(input_file):
     df = pd.read_csv(input_file)
     print("We will use the preprocessed csv fie.")
else:
    print("Processed file not found. Running Q1 preprocessing...")
    df = process_mati_data("mati.csv")

time_gap_df = pd.DataFrame()
time_gap_df=df.sort_values(['author_id','created_at'],ascending=[True, True])[['author_id', 'created_at']]
time_gap_df['created_at'] = pd.to_datetime(time_gap_df['created_at'])

#----q6_1------
time_gap_df['td_from_previous_tweet']=time_gap_df.groupby('author_id')['created_at'].diff()
#----q6_1------

time_gap_df['td_from_previous_tweet_in_minutes']=time_gap_df['td_from_previous_tweet'].dt.total_seconds()/60

#----q6_2.1------
#In order to find the mean we need at least 2 tweets because we need 1 or more gaps.
time_gap_df['average_time_gap']=time_gap_df.groupby('author_id')['td_from_previous_tweet_in_minutes'].transform('mean')
#----q6_2.1------
#----q6_2.2------
#In order to find std we need at least 3 tweets because we need 2 or more gaps.
time_gap_df['std_time_gap']=time_gap_df.groupby('author_id')['td_from_previous_tweet_in_minutes'].transform('std')
#----q6_2.2------


#like case when in tsql. Its a wildcard it can go whereever we want
time_gap_df['has_small_gap']=0
time_gap_df.loc[time_gap_df['td_from_previous_tweet_in_minutes']<1,'has_small_gap']=1
time_gap_df['gaps_under_1_minute']=time_gap_df.groupby('author_id')['has_small_gap'].transform('sum')
time_gap_df=time_gap_df.drop(columns=['has_small_gap'])

time_gap_df['has_large_gap']=0
time_gap_df.loc[time_gap_df['td_from_previous_tweet_in_minutes']>1440,'has_large_gap']=1
time_gap_df['gaps_more_than_a_date']=time_gap_df.groupby('author_id')['has_large_gap'].transform('sum')
time_gap_df=time_gap_df.drop(columns=['has_large_gap'])

#----q6_1_2_3---
time_gap_df.to_csv('q6_1_2_3.csv',index=False)
#----q6_1_2_3---
columns_from_time_gap=[ 'author_id','average_time_gap','std_time_gap','gaps_under_1_minute','gaps_more_than_a_date']

authors_analysis_df=time_gap_df[columns_from_time_gap].drop_duplicates('author_id')
authors_analysis_df=authors_analysis_df.sort_values('gaps_under_1_minute',ascending=[False])


authors_analysis_df.to_csv('q6_4.csv',index=False)