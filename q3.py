import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# ----------------------
# Load relevant tweets (Q1)
# ----------------------
df = pd.read_csv("data/mati_q1_relevant.csv") 

# ----------------------
# CALCULATE TWEET VOLUME PER AUTHOR
# ----------------------
# We group tweets per author
# and calculate number of tweets 
author_volume = (df.groupby("author_id").size().reset_index(name="total_tweets"))

# ----------------------
# THRESHOLD >= 3 tweets
# ----------------------
active_authors = author_volume[author_volume["total_tweets"] >= 3]["author_id"]

df_active = df[df["author_id"].isin(active_authors)].copy() # make copy to avoid warnings


print("Σύνολο authors:", author_volume.shape[0])
print("Ενεργοί authors (>=3 tweets):", df_active["author_id"].nunique()) #NUMBER of unique values(different authors)
print("Tweets που κρατήθηκαν:", len(df_active))
# ----------------------
# SUBQUESTION 3.1:
# Total tweets per active author
# ----------------------
#Calculate total number of tweets per active author and sort them in descending order.
author_tweet_counts = (
    df_active.groupby("author_id")
    .size()
    .reset_index(name="total_tweets")
    .sort_values("total_tweets", ascending=False))

print("\nTop 20 active authors by total tweets:")
print(author_tweet_counts.head(20))

print("\nBottom active authors (still >=3 tweets):")
print(author_tweet_counts.tail(20))

#---------------------------
# SUBQUESTION 3.2
#---------------------------
#without datetime:
#i can't leave out times
#there are no time metrics
df_active["created_at"] = pd.to_datetime(
    df_active["created_at"],
    utc=True,
    errors="coerce")   #create NaN values where datetime conversion is not possible in order to drop them later


df_active = df_active.dropna(subset=["created_at"]) #start and end point of each activity per author
                                                    #subset=to focus on created at line
author_time_span = (
    df_active
    .groupby("author_id")["created_at"] #group tweets of each author and look at datetime
    .agg(
        first_tweet="min",
        last_tweet="max")
    .reset_index()) #make list again

author_time_span["time_span_days"] = (
    author_time_span["last_tweet"] -
    author_time_span["first_tweet"]).dt.days #take only the day from the timedate 

author_time_span = author_time_span.sort_values(
    "time_span_days",
    ascending=False)

print("\nAuthors with largest activity time span:")
print(author_time_span.head(20))

print("\nAuthors with smallest activity time span:")
print(author_time_span.tail(20))

#-------------------------------------
# SUBQUESTION 3.3
#------------------------------------

df_active = df_active.sort_values(
    ["author_id", "created_at"]) #σορτάρω ανά author και μετά ανά ώρα
df_active["time_diff"] = (
    df_active
    .groupby("author_id")["created_at"]
    .diff())     # E.G created_at : 14:00 , 14:05 , 14:15 is made NaT , 5 minutes , 15 minutes
                 #finds:how often each author posts( ignores first tweet )

avg_time_gap = (
    df_active
    .groupby("author_id")["time_diff"]
    .mean()     #We calculate the average time interval between consecutive tweets for each author.
    .dt.total_seconds() / 60) # We use dt to take numeric values. (eg  00:15:00 becomes 900 seconds)and then divide by 60

avg_time_gap = avg_time_gap.reset_index(name="avg_time_gap_minutes")   #Give name to the list

print("\nAuthors with smallest avg time gap (very frequent posting):")
print(avg_time_gap.sort_values("avg_time_gap_minutes").head(20))

print("\nAuthors with largest avg time gap (sparse posting):")
print(avg_time_gap.sort_values("avg_time_gap_minutes", ascending=False).head(20))

#-------------------------------
# WEIGHTED SCORING SYSTEM
#----------------------------------

# MERGE OF ALL METRICS
author_stats = (
    author_tweet_counts
    .merge(author_time_span, on="author_id")   #Merging the tables
    .merge(avg_time_gap, on="author_id"))

# CLEAR VALUES
author_stats["avg_time_gap_minutes"] = (
    author_stats["avg_time_gap_minutes"]
    .fillna(author_stats["avg_time_gap_minutes"].median()) #fillna(median) -->«if im not aware of an author's gap 
    .replace(0, 0.1))  #I divide later                  # put a typical value»

# DEFINE WEIGHTED SCORE
author_stats["activity_score"] = (
    0.5 * np.log1p(author_stats["total_tweets"]) +
    0.3 * np.log1p(author_stats["time_span_days"] + 1) +
    0.2 * (1 / np.log1p(author_stats["avg_time_gap_minutes"])))
   #LOG so that values dont "break".We ingore spamming,but care about the active user
   
# RANKING AUTHORS
author_stats = author_stats.sort_values(
    "activity_score", ascending=False)

print("\nTop 20 authors by activity score:")
print(author_stats.head(20))

print("\nLeast active (still >=3 tweets):")
print(author_stats.tail(20))

# ----------------------
# TABLE: Top Active Authors
# ----------------------

top_authors = author_stats[[
    "author_id",
    "total_tweets",
    "time_span_days",
    "avg_time_gap_minutes",
    "activity_score"]].head(20)

print("\nTop 20 Most Active Authors:")
print(top_authors)

# Save for the report
top_authors.to_csv("data/q3_top20_active_authors.csv",index=False)

# ----------------------
#  scatter plot with mean line
# ----------------------

plot_df = author_stats.sort_values("total_tweets")

rolling_mean = (plot_df["activity_score"].rolling(window=50, center=True).mean())

plt.figure(figsize=(8, 6))

plt.scatter(plot_df["total_tweets"],plot_df["activity_score"],alpha=0.4)

plt.plot(plot_df["total_tweets"],rolling_mean,linewidth=3,color='red',label="Mean Trend")

plt.xlabel("Total Tweets per Author")
plt.ylabel("Activity Score")
plt.title("Author Activity with Mean Trend Line")
plt.legend()
plt.tight_layout()
plt.savefig("plots/q3_scatter_with_trend.png")
plt.show()