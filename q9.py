import os
import pandas as pd
from q1 import process_mati_data
from q2 import burst_df_creation

input_file="data/mati_q1_relevant.csv"
if os.path.exists(input_file):
     df=pd.read_csv(input_file)
     print("We will use the preprocessed csv fie.")
else:
    print("Processed file not found. Running Q1 preprocessing...")
    df=process_mati_data("mati.csv")

input_burst_info="q2_burst_info.csv"
if os.path.exists(input_burst_info):
     q2_burst_info_df=pd.read_csv(input_burst_info)
     print("We will use the q2_burst_info csv fie.")
else:
     print("q2_burst_info file not found. Running Q2 in order to create it...")
     q2_burst_info_df,day_min,day_max = burst_df_creation(df)


#We find the dates that there is a burst
filtered_burst_info_df= q2_burst_info_df[q2_burst_info_df['burst'] == True]

#we export the dates of the bursts
burst_dates=filtered_burst_info_df[['dates']].copy()
#We find the tweets of these days
filtered_df_by_burst= df[df['dates'].isin(burst_dates['dates'])].copy()
filtered_df_by_burst=filtered_df_by_burst.sort_values('created_at')
#----------q9_1 result-----------
filtered_df_by_burst.to_csv("q9_1_busts_tweets_only.csv",index=False)
#----------q9_1 result-----------

#We find the tweets of 6 hours before each burst(one day) so we need the hours(18:00-00:00) of the day before
burst_dates['dates']=pd.to_datetime(burst_dates['dates'], utc=True)
df['created_at']=pd.to_datetime(df['created_at'], utc=True)
burst_dates['from_time']=pd.to_datetime(burst_dates['dates'])-pd.Timedelta(hours=6)
burst_dates['to_time']=burst_dates['dates']

#join the two dataframes
df['key']=1
burst_dates['key']=1
merged_df=pd.merge(df,burst_dates, on='key')

tweets_six_hours_before_burst=merged_df[(merged_df['created_at']>=merged_df['from_time'])&(merged_df['created_at']<merged_df['to_time'])].copy()
del df['key']
del burst_dates['key']
tweets_six_hours_before_burst=tweets_six_hours_before_burst.drop(columns=['key'])

#dentify the most active authors(10) 6 hours before a burst
counts_tweets_per_author=tweets_six_hours_before_burst.groupby(['to_time','author_id']).size().reset_index(name='tweet_count')
counts_tweets_per_author_sorted=counts_tweets_per_author.sort_values(['to_time','tweet_count'],ascending=[True, False])
counts_tweets_per_author_sorted=counts_tweets_per_author_sorted.groupby('to_time').head(10)

#----------q9_2 result-----------
counts_tweets_per_author_sorted.to_csv('q9_2_counts_tweets_per_author_per_burst.csv',index=False)
#----------q9_2 result-----------


count_tweets_per_author_per_burst=filtered_df_by_burst.groupby(['author_id','dates'], as_index=False).agg(tweets=('dates', 'size'))
daily_totals=count_tweets_per_author_per_burst.groupby('dates')['tweets'].sum().reset_index(name='daily_total_tweets')
count_tweets_per_author_per_burst=pd.merge(count_tweets_per_author_per_burst, daily_totals, on='dates', how='left')

#----------q9_3.1 result-----------
count_tweets_per_author_per_burst['tweets_perc_per_author']=(count_tweets_per_author_per_burst['tweets']/count_tweets_per_author_per_burst['daily_total_tweets'])*100
#----------q9_3.1result-----------

first_tweet_of_author=filtered_df_by_burst.groupby(['dates','author_id'])['created_at'].min().reset_index(name='first_author_tweet_date')

count_tweets_per_author_per_burst = pd.merge(
    count_tweets_per_author_per_burst, 
    first_tweet_of_author, 
    on=['dates', 'author_id'], 
    how='left'
)
count_tweets_per_author_per_burst['dates']=pd.to_datetime(count_tweets_per_author_per_burst['dates'], utc=True)
count_tweets_per_author_per_burst['first_author_tweet_date']=pd.to_datetime(count_tweets_per_author_per_burst['first_author_tweet_date'], utc=True)
#----------q9_3.2 result-----------
count_tweets_per_author_per_burst['lag']=count_tweets_per_author_per_burst['first_author_tweet_date']-count_tweets_per_author_per_burst['dates']
#----------q9_3.2 result-----------

count_tweets_per_author_per_burst.to_csv('q9_2_3.csv',index=False, float_format='%.5f')


count_tweets_per_author_per_burst['rank_vol']=count_tweets_per_author_per_burst.groupby('dates')['tweets_perc_per_author'].rank(ascending=False)
count_tweets_per_author_per_burst['rank_lag']=count_tweets_per_author_per_burst.groupby('dates')['lag'].rank(ascending=True)
count_tweets_per_author_per_burst['burst_score']=(count_tweets_per_author_per_burst['rank_vol']+count_tweets_per_author_per_burst['rank_lag'])/2

key_drivers=count_tweets_per_author_per_burst.groupby('author_id').agg(total_bursts_participated=('dates', 'count'),avg_burst_score=('burst_score','mean'),avg_contribution=('tweets_perc_per_author','mean')).reset_index()
ranked_df=key_drivers.sort_values(by=['total_bursts_participated','avg_burst_score'],ascending=[False, True])
#----------q9_4 result-----------
ranked_df.to_csv('q9_4.csv')
#----------q9_4 result-----------


#----------q9_4 result-----------
ranked_df_for_q9_2_authors=ranked_df[ranked_df['author_id'].isin(counts_tweets_per_author_sorted['author_id'])].copy()
ranked_df_for_q9_2_authors.to_csv('q9_4_alter.csv')
#----------q9_4 result-----------