import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

def load_data():
    tweets_df = pd.read_csv("data/mati_q1_relevant.csv")
    burst_df = pd.read_csv("data/q2_burst_info.csv")
    author_retweet_df = pd.read_csv("data/author_retweet_dependency.csv")
    return tweets_df, burst_df, author_retweet_df

# Coordinated activity
def analyze_coordination_patterns(tweets_df, burst_df, author_retweet_df):       
    tweets_df['created_at'] = pd.to_datetime(tweets_df['created_at'], utc=True)
    tweets_df['date'] = tweets_df['created_at'].dt.date.astype(str)
    tweets_df['hour'] = tweets_df['created_at'].dt.hour
    
    # Get burst tweets
    burst_dates = burst_df[burst_df['burst'] == True]['dates'].tolist()
    burst_tweets = tweets_df[tweets_df['date'].isin(burst_dates)].copy()
    
    # Count tweets per author during bursts
    author_burst_counts = burst_tweets.groupby('author_id').size().reset_index(name='burst_tweets')
    
    # Add retweet dependency from Q8
    author_burst_counts = author_burst_counts.merge(
        author_retweet_df[['author_id', 'retweet_dependency']], 
        on='author_id', how='left'
    ).fillna(0)
    
    # Look for synchronized posting (5-min window)
    burst_tweets['time_bucket'] = burst_tweets['created_at'].dt.floor('5min')
    bucket_counts = burst_tweets.groupby('time_bucket').size()
    threshold = bucket_counts.quantile(0.90)
    high_activity_buckets = bucket_counts[bucket_counts > threshold].index
    
    # count how often each author appears in high-activity windows
    high_tweets = burst_tweets[burst_tweets['time_bucket'].isin(high_activity_buckets)]
    sync_counts = high_tweets.groupby('author_id').size().reset_index(name='sync_appearances')
    
    author_burst_counts = author_burst_counts.merge(sync_counts, on='author_id', how='left').fillna(0)
    
    # calculate coordination score (score=0.3*volume + 0.4*dependency + 0.3*synchronisation)
    author_burst_counts['score'] = (
        author_burst_counts['burst_tweets'] / author_burst_counts['burst_tweets'].max() * 0.3 +
        author_burst_counts['retweet_dependency'] / 100 * 0.4 +
        author_burst_counts['sync_appearances'] / (author_burst_counts['sync_appearances'].max() + 1) * 0.3
    )
    
    # sort
    author_burst_counts = author_burst_counts.sort_values('score', ascending=False)
    author_burst_counts.to_csv('data/q10_2_coordination_scores.csv', index=False)
    
    # Get the specific list of authors by ordering the score
    top_authors_ordered = author_burst_counts.head(30)['author_id'].tolist()
    top_tweets = burst_tweets[burst_tweets['author_id'].isin(top_authors_ordered)]
    
    # matrix
    heatmap_data = top_tweets.groupby(['author_id', 'hour']).size().unstack(fill_value=0)
    
    # Reindex so rows match the sorted 'top_authors_ordered' list
    heatmap_data = heatmap_data.reindex(top_authors_ordered)
    
    plt.figure(figsize=(14, 10))
    sns.heatmap(heatmap_data, cmap='YlOrRd', linewidths=0.5)
    plt.xlabel('Hour of Day')
    plt.ylabel('Author ID (Sorted by Score)')
    plt.title('Hourly Activity During Bursts')
    plt.tight_layout()
    plt.savefig('plots/coordinated_activity_heatmap.png', dpi=150)
    plt.close()
    
    return author_burst_counts

if __name__ == "__main__":
    tweets_df, burst_df, author_retweet_df = load_data()
    coordination_df = analyze_coordination_patterns(tweets_df, burst_df, author_retweet_df)