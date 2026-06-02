import os
import pandas as pd
from q1 import process_mati_data
from q2 import burst_df_creation

def load_data():
    input_file = "data/mati_q1_relevant.csv"
    if os.path.exists(input_file):
        df=pd.read_csv(input_file)
        print("We will use the preprocessed csv fie.")
    else:
        print("Processed file not found. Running Q1 preprocessing...")
        df=process_mati_data("mati.csv")

    input_burst_info="q2_burst_info.csv"
    if os.path.exists(input_burst_info):
        q2_burst_info_df = pd.read_csv(input_burst_info)
        print("We will use the q2_burst_info csv fie.")
    else:
        print("q2_burst_info file not found. Running Q2 in order to create it...")
        q2_burst_info_df,day_min,day_max = burst_df_creation(df)

    return df,q2_burst_info_df


def find_possible_catalysts(df, q2_burst_info_df):

    filtered_burst_info_df= q2_burst_info_df[q2_burst_info_df['burst'] == True]

    burst_dates = filtered_burst_info_df[['dates']].copy()
    burst_dates['dates']=pd.to_datetime(burst_dates['dates'], utc=True)
    df['created_at']=pd.to_datetime(df['created_at'], utc=True)
    burst_dates['from_time']=pd.to_datetime(burst_dates['dates'])-pd.Timedelta(hours=6)
    burst_dates['to_time']=burst_dates['dates']
    df['key']=1
    burst_dates['key']=1
    merged_df=pd.merge(df, burst_dates, on='key')

    tweets_six_hours_before_burst=merged_df[(merged_df['created_at']>=merged_df['from_time']) &(merged_df['created_at']<merged_df['to_time'])].copy()
    del df['key']
    del burst_dates['key']
    tweets_six_hours_before_burst=tweets_six_hours_before_burst.drop(columns=['key'])
 
    counts_tweets_per_author=tweets_six_hours_before_burst.groupby(['to_time','author_id']).agg( tweet_count=('created_at','size'),time_of_latest_tweet=('created_at','max')).reset_index()
    counts_tweets_per_author_sorted=counts_tweets_per_author.sort_values(['to_time','tweet_count'],ascending=[True, False])

    counts_tweets_per_author_sorted['time_of_latest_tweet']=pd.to_datetime(counts_tweets_per_author_sorted['time_of_latest_tweet'], utc=True)
    counts_tweets_per_author_sorted['to_time']=pd.to_datetime(counts_tweets_per_author_sorted['to_time'], utc=True)
    time_threshold=counts_tweets_per_author_sorted['to_time']-pd.Timedelta(hours=1)
    
    catalysts=counts_tweets_per_author_sorted[counts_tweets_per_author_sorted['time_of_latest_tweet']>=time_threshold].copy()    

     #----------q10_2 result-----------
    catalysts.to_csv('q10_1_catalysts_author.csv', index=False)
    #----------q10_2 result-----------


if __name__ == "__main__":
    df, q2_burst_info_df = load_data()
    find_possible_catalysts(df, q2_burst_info_df)
