import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os
from q1 import process_mati_data

os.makedirs("plots", exist_ok=True)

def generate_three_diagrams():
    input_file = "data/mati_q1_relevant.csv"
    if os.path.exists(input_file):
        df = pd.read_csv(input_file)
    else:
        df = process_mati_data("mati.csv")
    
    # RTs
    df['is_retweet'] = df['text'].astype(str).str.contains(r'^RT\s', regex=True, na=False)
    
    # author statistics
    author_stats = df.groupby('author_id').agg(
        total_tweets=('text', 'count'),
        retweet_count=('is_retweet', 'sum')
    ).reset_index()
    
    # RT dependency
    author_stats['retweet_percentage'] = (author_stats['retweet_count'] / author_stats['total_tweets']) * 100

    # Pie Chart
    total_retweets = df['is_retweet'].sum()
    total_original = len(df) - total_retweets
    
    plt.figure(figsize=(7, 7))
    plt.pie(
        [total_retweets, total_original], 
        labels=[f'Retweets\n({total_retweets})', f'Original\n({total_original})'], 
        autopct='%1.1f%%', 
        colors=['#ff9999', '#66b3ff'], 
        startangle=140,
        explode=(0.05, 0)
    )
    plt.title('Global Percentage of Retweets in Dataset')
    plt.savefig('plots/diagram1_global_retweet_percent.png')
    plt.close() # Good practice to close figure to free memory

    # RT distribution histogram
    plt.figure(figsize=(10, 6))
    sns.histplot(
        author_stats['retweet_percentage'], 
        bins=20, 
        kde=False, 
        stat="count",
        color='mediumpurple'
    )
    plt.title('Distribution of Author Retweet Dependency')
    plt.xlabel('Retweet Percentage (0% = Original, 100% = Pure RT)')
    plt.ylabel('Number of Authors')
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.savefig('plots/diagram2_author_dependency_hist.png')
    plt.close()

    # Scatter plot for users
    plt.figure(figsize=(10, 6))
    
    sns.scatterplot(
        data=author_stats,
        x='total_tweets',
        y='retweet_percentage',
        alpha=0.5,
        color='teal',
        s=30
    )
    
    plt.title('Activity Volume vs. Retweet Dependency')
    plt.xlabel('Total Tweets Posted (Log Scale)')
    plt.ylabel('Retweet Percentage (%)')
    plt.xscale('symlog')
    plt.grid(True, linestyle='--', alpha=0.3)
    plt.savefig('plots/diagram3_volume_vs_dependency.png')
    plt.show()
    plt.close()

if __name__ == "__main__":
    generate_three_diagrams()