# ----------------------
# Question 5 – Engagement Metrics Aggregation
# ----------------------

# ----------------------
#LIBRARIES
# ----------------------

import pandas as pd
import matplotlib.pyplot as plt
import os

# ----------------------
# SETTINGS
# ----------------------
DATA_FILE = "data/mati_q1_relevant.csv"
PLOTS_DIR = "../plots"
os.makedirs(PLOTS_DIR, exist_ok=True)

# ----------------------
# LOAD DATA
# ----------------------
df = pd.read_csv(DATA_FILE)

print(" Loaded relevant tweets:", df.shape)

# ----------------------
# CLEAN COUNTS
# ----------------------
engagement_cols = ["like_count","retweet_count","reply_count"]
#engagement_cols = ["like_count","retweet_count","reply_count","quote_count"]

df[engagement_cols] = df[engagement_cols].fillna(0) #In case i do not have a metric (eg like)

# ----------------------
# TOTAL ENGAGEMENT PER TWEET
# ----------------------
df["total_engagement"] =(df["like_count"] +df["retweet_count"] +df["reply_count"])   #It needs to be alltogether( aggregate )
'''
df["total_engagement"] = (
    df["like_count"] +
    df["retweet_count"] +
    df["reply_count"] +
    df["quote_count"])            # aggregate 
'''

print("\n Engagement per tweet (sample):")
print(df[["total_engagement"]].head())

# ----------------------
#AGGREGATION PER AUTHOR
# ----------------------
author_engagement = (
    df.groupby("author_id") #group by author
    .agg(                                      
        total_tweets=("tweet_id", "count"),     #tweets per author
        total_likes=("like_count", "sum"),     #add all likes from tweets of the author
        total_retweets=("retweet_count", "sum"), #total retweet
        total_replies=("reply_count", "sum"),    #total reply
        #total_quotes=("quote_count", "sum"),       #total quotes
        total_engagement=("total_engagement", "sum"),   #add all the engagement of step 3
        avg_engagement_per_tweet=("total_engagement", "mean"))   #mean engagement per tweet
    .reset_index())                                     #make list

author_engagement = author_engagement.sort_values(
    "total_engagement", ascending=False)

print("\n Top 10 authors by total engagement:")
print(author_engagement.head(10))

# ----------------------
# SAVE TABLE
# ----------------------
author_engagement.to_csv("data/q5_author_engagement_metrics.csv",index=False)

# ----------------------
# DATASET-LEVEL ENGAGEMENT DISTRIBUTION
# ----------------------
'''
Calculating total engagement of all relevant tweets.
Answer to – Total counts for like count, retweet count, and reply count.
'''
total_metrics = {
    "Likes": df["like_count"].sum(),
    "Retweets": df["retweet_count"].sum(),
    "Replies": df["reply_count"].sum()}
    #"Quotes": df["quote_count"].sum()}
 
plt.figure(figsize=(7, 7))   #Round
plt.pie(
    total_metrics.values(),
    labels=total_metrics.keys(),
    autopct="%1.1f%%",
    startangle=140)

plt.title("Engagement Metrics Distribution (All Relevant Tweets)")
plt.tight_layout()
plt.savefig(f"{PLOTS_DIR}/q5_engagement_distribution.png")
plt.show()

# ----------------------
# AUTHOR ENGAGEMENT SCATTER
# ----------------------
plt.figure(figsize=(8, 6))
plt.scatter(
    author_engagement["total_tweets"],         # X-axis
    author_engagement["total_engagement"],      #Y-axis
    alpha=0.5)

plt.xlabel("Total Tweets per Author")
plt.ylabel("Total Engagement")
plt.title("Author Activity vs Engagement")
plt.tight_layout()
plt.savefig(f"{PLOTS_DIR}/q5_author_activity_vs_engagement.png")
plt.show()

print("Total likes:", df["like_count"].sum())
print("Total retweets:", df["retweet_count"].sum())
print("Total replies:", df["reply_count"].sum())
print("Total quotes:", df["quote_count"].sum())
print("\n Question 5 completed")

print("\n Question 5 completed")
