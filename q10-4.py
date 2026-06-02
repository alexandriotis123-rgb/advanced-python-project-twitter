import os
import re
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

def load_data():
    tweets_df = pd.read_csv("data/mati_q1_relevant.csv")
    burst_df = pd.read_csv("data/q2_burst_info.csv")
    author_retweet_df = pd.read_csv("data/author_retweet_dependency.csv")
    return tweets_df, burst_df, author_retweet_df

def analyze_network_roles(rt_stats):
    sns.set_theme(style="whitegrid")

    active_authors = rt_stats[rt_stats['total_retweets'] > 5].copy()
    
    # categorize the amplification score
    conditions = [
        (active_authors['burst_amplification'] <= 1.5),
        (active_authors['burst_amplification'] > 1.5) & (active_authors['burst_amplification'] < 3.5),
        (active_authors['burst_amplification'] >= 3.5)
    ]

    categories = ['Normal Activity', 'Mixed Activity', 'Suspicious activity']
    active_authors['Behavior Category'] = np.select(conditions, categories, default='Mixed/Elevated Activity')
    
    # Convert to categorical type to ensure legend order
    active_authors['Behavior Category'] = pd.Categorical(
        active_authors['Behavior Category'], 
        categories=categories, 
        ordered=True
    )

    category_palette = {
        'Normal Activity': '#3498db',
        'Suspicious activity': '#e74c3c',
        'Mixed Activity': '#95a5a6'
    }

    plt.figure(figsize=(11, 9))
    sns.scatterplot(
        data=active_authors, 
        x='normal_retweets', 
        y='burst_retweets', 
        hue='Behavior Category',
        palette=category_palette,
        size='total_retweets',
        sizes=(30, 600),
        alpha=0.75,
        edgecolor='w', linewidth=0.5
    )
    
    # diagonal reference line (y=x) burst tweets = normal tweets
    max_val = max(active_authors['normal_retweets'].max(), active_authors['burst_retweets'].max())
    plt.plot([0, max_val], [0, max_val], ls="--", c=".4", alpha=0.5, label='Balanced Activity Line (y=x)')
    
    # Log scale
    plt.xscale('symlog', linthresh=1)
    plt.yscale('symlog', linthresh=1)
    plt.title('Users by Burst Participation', fontsize=14, pad=20)
    plt.xlabel('Volume during Normal Periods', fontsize=11)
    plt.ylabel('Volume during Bursts', fontsize=11)
    
    handles, labels = plt.gca().get_legend_handles_labels()
    legend = plt.legend(handles=handles, labels=labels, bbox_to_anchor=(1.02, 1), loc=2, borderaxespad=0., frameon=False)
    legend.set_title("User Behavior & Total Volume")

    plt.grid(True, which="minor", ls=":", alpha=0.3)
    plt.tight_layout()
    plt.savefig('plots/network_roles.png', dpi=150, bbox_inches='tight')
    plt.close()

# RT during bursts
def analyze_burst_retweet_patterns(tweets_df, burst_df, author_retweet_df):
    # Ensure output directory exists
    os.makedirs('data', exist_ok=True)
    os.makedirs('plots', exist_ok=True)

    tweets_df['created_at'] = pd.to_datetime(tweets_df['created_at'], utc=True)
    tweets_df['date'] = tweets_df['created_at'].dt.date.astype(str)
    tweets_df['is_retweet'] = tweets_df['text'].astype(str).str.contains(r'^RT\s', regex=True, na=False)
    
    # Extract RT'd author
    def extract_retweeted_author(text):
        if pd.isna(text):
            return None
        match = re.match(r'^RT\s+@(\w+):', str(text))
        return match.group(1).lower() if match else None
    
    # add a column of the RT'd author
    tweets_df['retweeted_author'] = tweets_df['text'].apply(extract_retweeted_author)
    
    # Get burst dates
    burst_dates = burst_df[burst_df['burst'] == True]['dates'].tolist()
    tweets_df['is_burst_day'] = tweets_df['date'].isin(burst_dates)
    
    # Count retweets per author during burst vs non-burst
    retweets = tweets_df[tweets_df['is_retweet'] & tweets_df['retweeted_author'].notna()].copy()
    
    # Sort RT'd author in bursts
    burst_rt = retweets[retweets['is_burst_day']].groupby('retweeted_author').size()
    normal_rt = retweets[~retweets['is_burst_day']].groupby('retweeted_author').size()
    
    # Dataframe for bursts RTs and normal time RTs
    rt_stats = pd.DataFrame({
        'burst_retweets': burst_rt,
        'normal_retweets': normal_rt
    }).fillna(0).astype(int)
    
    rt_stats['total_retweets'] = rt_stats['burst_retweets'] + rt_stats['normal_retweets']
    
    total_days = len(burst_df)
    n_burst_days = len(burst_dates) 
    burst_time_share = n_burst_days / total_days if total_days > 0 else 0
    
    # percentage of an author's RTs that happened during bursts
    rt_stats['user_burst_share'] = rt_stats['burst_retweets'] / rt_stats['total_retweets']
    
    # Lift -> How many times more likely is a retweet during burst vs random?
    if burst_time_share > 0:
        rt_stats['burst_amplification'] = rt_stats['user_burst_share'] / burst_time_share
    else:
        rt_stats['burst_amplification'] = 0

    # >= 5 
    significant = rt_stats[rt_stats['total_retweets'] >= 5].sort_values('burst_amplification', ascending=False)
    significant.to_csv('data/q10_2_burst_amplification.csv')
    
    # we sort by contribution to brust RTs
    top20 = rt_stats.sort_values('burst_retweets', ascending=False).head(20).reset_index()
    
    plt.figure(figsize=(12, 8))
    x = np.arange(len(top20))
    width = 0.35
    
    # Plotting Horizontal Bars
    plt.barh(x - width/2, top20['burst_retweets'], width, label='During Bursts', color='#e74c3c')
    plt.barh(x + width/2, top20['normal_retweets'], width, label='Normal Periods', color='#3498db')
    
    plt.yticks(x, top20['retweeted_author'], fontsize=9)
    plt.xlabel('Number of Retweets')
    plt.title('Top Authors by Burst Volume')
    plt.legend()
    plt.tight_layout()
    plt.savefig('plots/burst_amplification.png', dpi=150)
    plt.close()

    analyze_network_roles(rt_stats)
    
    return significant, tweets_df

if __name__ == "__main__":
    tweets_df, burst_df, author_retweet_df = load_data()
    amplification_df, tweets_df = analyze_burst_retweet_patterns(tweets_df, burst_df, author_retweet_df)