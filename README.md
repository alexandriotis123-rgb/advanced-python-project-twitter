# Advanced_Programming_Final
This is the technical report for the APP final project 2025-2026 Advanced Python Programming. Here you will find:

1. All the python code required for the assignment.
2. All the csvs created for the needs of the assignment, in the relevant directory
3. All the plots in the relevant directory
4. requirements.txt for all the required libraries used in the assignment
5. The final LATEX report that presents our findings in a more formal manner

names: GERASIMOS PAPANIKOLAOU-NTAIS, ALEXANDROS ANDRIOTIS, IOANNIS MAKRYGIANNAKIS

-------------------------------------------------------------------------------------
q1: 
-The goal of Question 1 was to distinguish the relevant tweets in the raw dataset
 that truly had relation to the Mati wildfire.
 -Unrelated tweets that mention similar keywords had to be removed( e.g songs,other wildfires )
 -A critical step for the subsequent questions, as they use the filtered list of relevant tweets for further actions

 We filtered each tweet :
 1) Text preprocess
 2) Greek language filtering
 3) Lemmatization

 Followed by a keyword selection of a location term (e.g Mati , rafina ) AND
 an event/authority/casualty keyword

 From approximately 300.000 tweets,
 around 27% was relevant tweets.

 NOTES
 -This keyword selection method prioritizes precision over quantity
  to ensure better results in the following questions

RUN_LEMMATIZATION =True
 True: to run Lemmatization
 False: to skip it

DEBUG_SAMPLES = True
True: to run samples of relevant/irrelevant tweets
False: to skip this step
 
SAVE_PREPROCESSED=True
True if you wish to save the file

---------------------------------------------------------------------------------------
q2:
In this file, we perform a statistical analysis on the daily volume of tweets to identify bursts based on a calculated threshold. For this analysis, each burst is defined as a single day.
To achieve this, we follow the steps below for each sub-question:
q2.1)
 -We check if the file mati_q1_relevant.csv exists. If not, we rerun the script for Question 1 (preprocessing step).
 -We use the 'created_at' column to group the tweets by date.
 -Finally, we identify the dates that do not have tweets (missing dates) and assign them a volume of 0.
q2.2, q2.3)
 -We create two new columns in the dataframe named rolling_mean and rolling_std.
 -We compute the rolling mean and rolling standard deviation based on a 7-day window.
 -Finally, we define a threshold calculated as: rolling_mean + (2 * rolling_std).
q2.4)
 -We identify daily bursts by comparing the threshold with the daily tweet volume. If the volume exceeds the threshold limit, we flag it as a burst.
 -Finally, we create two time-series plots: one that displays the daily volume, rolling average, and threshold, and another that visualizes all the previous columns and the daily bursts of tweets over time.

---------------------------------------------------------------------------------------
q3:
The main goal for Question 3 was to analyze activity patterns of Twitter authors and compute some metrics.
We aim to identify the highest ranked authors and rank them based on a weighted activity score.

-File used: mati_q1_relevant.csv

        Subquestion 3.1 : Total tweets per author

- Group tweets by author.
- Count tweets each author had.
- Apply a threshold (>=3 tweets) to remove noise.

        Subquestion 3.2 :Time span per author
-Goal:Measure the longevity of each author (How long each author was active in the dataset)

The method to accomplish that is to:
-Identify the first tweet timestamp for each author
-Identify the last tweet timestamp for each author
-Calculate the difference in days

Result:
-Large span = sustained involvement over time
-Short span= possible burst-like behavior
-Zero span = One day activity!

        Subquestion 3.3 : Average time interval between consecutive tweets

-Estimation of the frequency of tweets for each author

The main method is to:
-Sort tweets by author and time
-Calculate time difference between posts
-The mean time gap is calculated IN MINUTES

This is essential because it captures intensity:
 -2 authors may both have 30 tweets but if one of them posted all of them in 2 hours,
 -that means he has high intensity,while the other author posted them in 1 month(low intensity)

        Subquestion 3.4 : Weighted Scoring System

Goal is to combine all the metrics above to rank the authors
-Calculated using logarithms ( activity_score )
-Without logarithms,Spammers dominated the graphs
-Also,using logarithms ,we stabilize extreme values and make the results smoother.

-Saved top 20 authors

        Subquestion 3.5: Provide visualizations.

Scatter plot: Each blue point represents an author
-Highlights active users. Authors with high score
is not always relevant to the fact that they have many tweets in total.
-Helpful plot to detect spams, bots and outliers.

---------------------------------------------------------------------------------------
q4:
In this file we do the temporal analysis on the dataset. 
- Calculates the average volume of tweets for each hour of the day. (hourly_counts = df.groupby(['date', 'hour']).size().reset_index(name='count')) and (avg_activity = hourly_counts.groupby('hour')['count'].mean().reset_index()).
- This normalises the data. Otherwise significant days, like the day the Mati incident happened, would dominate the entire plot and statistics.
- It creates a bar plot with the average activity for time per day.

---------------------------------------------------------------------------------------
q5:
-The main Goal of Question 5 was to analyze the interaction of users to the wildfire of Mati
using metrics provided by twitter( likes, retweets, replies)
This analysis is focused on these metrics and the engagement rate of authors

This analysis uses the filtered data of relevant tweets from Question 1

Method:
-Missing values on engagement_cols are replaced with zero to ensure correct calculations.
-Total engagement per tweet is calculated as (likes + retweets + relpies)
- Engagement metrics aggregated per author (tweets,likes,retweets,replies,engagement,avg engagement per tweet)

 Results are saved in a csv file and there are 2 visualizations (scatter plot+pie chart )

 IMPORTANT NOTES:
 1) quote counts were left as a comment section in the code because they were not included in the question
 and also Total quotes counts is significantly lower than the other metrics
 making the category irrelevant enough.
 2) Retweet count appears to dominate the engagement (90%)
 which is justified by the fact that they were formed during a crisis related event.
 This comes to the conclusion that users amplify information and there are a few authors that are influential.

---------------------------------------------------------------------------------------
q6: 
In this file, we analyze the behavior of users by calculating the time intervals between their consecutive tweets.
To achieve this, we follow the steps below for each sub-question:
q6.1)
     -We check if the file mati_q1_relevant.csv exists. If not, we rerun the script for Question 1 (preprocessing step).
     -We sort the data by author_id and created_at to ensure chronological order per user.
     -We calculate the time difference between each tweet.
q6.2_1, 6.2_2)
    - We calculate the average time gap and the standard deviation for each author. In order to do that we need a minimum of 2 tweets is required for a mean gap
      and 3 tweets for a standard deviation.
q6.2_3)
    -We create 2 flags (has_small_gap,has_large_gap) in order to categorize gaps based on specific time:
        Small Gaps: Gaps under 1 minute.
        Large Gaps: Gaps exceeding 24 hours (1440 minutes).
    -We add the results to two collumns and delete the flags
    -Finally we export the results of q6.2 at a csv file (q6_1_2_3.csv).
q6.4)
    -We create a summary dataframe (authors_analysis_df) containing unique records for each author.
    -We sort the authors based on the frequency of their small gaps to highlight the most active.
    -Finally we export the results of q6.4 at a csv file (q6_4.csv.csv).


---------------------------------------------------------------------------------------
q7:
In this file we do again temporal analysis but weekly. 
- Here we generate a heatmap to spot generic activity patterns.
- We order the days of the week so its readable and understandable.
- In rows we have the week number of the timeline, in columns the days of the week and the cell color indicates the activity.

---------------------------------------------------------------------------------------
q8: 
In this file we perform originality analysis, meaning we calculate the RT dependency.
- We create 3 charts:
    1. Pie chart: generic to see what percentage of tweets are RTs or not for the entire dataset
    2. Dependency score plot: we group by author_id and calculate a dependency score ((RTs/total tweets) * 100). We can easily understand that a very high score (for example 90% or higher) indicates that either the user is lazy and just RTs things he agrees with or is a bot/troll.
    3. Author volume: we use the dependency score again, to create a scatter plot in a logarithmic scale to identify clusters of users that are just acting like bots or if the generate original content and/or RT.
These visualizations are revealing to the network manipulation. The top-right corner of the scatter plot shows a huge cluster of bots/amplifiers while the bottom right corner shows a smaller cluster of users generating original content, while on the center we see mostly normal users with mixed activity. (we use the logarithmic scale to enable us to visualize the massive difference of users (by spreading the data). For example, most users make 0-1-a few tweets and dominate the dataset while the amplifiers/bots may be fewer but generate most of the traffic)

---------------------------------------------------------------------------------------
q9:
In this file we  find the authors of tweets that are key drivers of activity during the daily bursts.
To achieve this, we follow the steps below for each sub-question:
q9.1) 
    -We check if the file "mati_q1_relevant.csv" exists. If not, we rerun the script for Question 1 (preprocessing step).
    -We check if the file "q2_burst_info.csv" exists. If not, we rerun the script for Question 2.
    -We identify the dates where a burst occurred and export them to a new dataframe (burst_dates).
    -Finally, we find the tweets posted on burst days.
q9.2)
    -Since each burst spans a full day, we examine the time window 18:00–00:00 on the day prior to each burst.
    -Then, we merge the "df" and "burst_dates" dataframes to create a new dataframe containing only the tweets from the preceding window.
    -We count the tweets per author for each burst and select only the top 10 for each day. Finally, we create a CSV file with them.
q9.3_1)
    -We find the volume contribution of each author for every burst.(The percentage of daily tweets belonging to each author.)
q9.3_2)
     -In order to find the lag time for each author we identify the exact timestamp of his first tweet posted on the burst day.
     -We calculate the lag by finding the time difference between the start of the day (00:00) and the author's first tweet.
     -Finally, we export the data to a CSV file named "q9_2_3.csv".
q.4)
    In order to find the key drivers of activity during the burst we need to create 3 columns inside the above dataframe. The rank_vol (volume contribution), the rank_lag (fastest reactio).
    -We calculate the "burst score" for each author by averaging their volume rank and lag rank.
    -We group the data by author to calculate the total number of bursts they participated in and their average burst score across all events.
    -Finally, we sort the authors by participation frequency and average burst score (ascending) to identify them and export them to "q9_4.csv".
    Now in case that the question ask us to find only the authors that has also tweets inside the time window 18:00–00:00 on the day prior to each burst, we create one q9_4_alter.csv.

Due to ambiguity regarding the scope of sub-questions 3 and 4, we generated two distinct datasets to cover both possible interpretations of the user base.
The file q9_4.csv includes all users who tweeted during the identified burst periods,
while q9_4_alter.csv focuses specifically on users who were active within the 6-hour window preceding each burst.

---------------------------------------------------------------------------------------
q10.1)
In this file we proccess the q9_4.csv file from question 9 in order to rank to isolate the top 1% of participants.In order to do that we follow the nexts steps:
    -We load the file "q9_4.csv".
    -We filter the dataset to identify the top 1% of most active authors (based on the ranking from Q9). It specifically captures their frequency 
     of participation in 'bursts' alongside their average contribution level.
    -We export the results in a new csv file so the final output provides a refined list of high-impact authors.

q10.2)
In this file, we identify "Catalyst" authors those whose activity likely triggered the bursts identified. In order to do that we follow the nexts steps:
    -We check for the existence of preprocessed data (mati_q1_relevant.csv).If not, we rerun the script for Question 1.
    -We check for the existence of q2_burst_info.csv .If not, we rerun the script for Question 1.
    -We isolate the 6-hour window immediately preceding each activity burst.
    -We aggregate tweet counts per author within these windows. To qualify as a Possible Catalyst, an author must have posted at least one tweet
     within the final 1 hour before the burst started.
    -Finally we export the results to a csv that contains the authors ranked by their recency for each burst event.

---------------------------------------------------------------------------------------
q10-3: 
This file identifies and creates visualizations for coordinated activity. It calculates a coordination score for every user to identify patterns (bots or paid trolls) that flood Twitter with RTs in a coordinated manner.
- We analyze Burst days that were identified in q2 & q9. We consider normal days irrelevant and not statistically important for the question of the assignment. 
- We calculate the 3 important metrics: volume (how many tweets in a burst, indicating that posting only in bursts consists of suspicious activity), RT dependency (percentage of user's tweets that are RTs, extremely high RT activity is suspicious), coordination (we divide the timeline into 5 min periods (keep busiest 10%) and count how many times a user posted in these periods, meaning that many tweets in such sort periods of time prove some form of coordination)
- We create a formula to identify coordination and scale (0-1) users according to these 3 metrics: score = 0.3*volume + 0.4*dependency + 0.3*coordination
- This formula helps us identify users with high coordination, meaning the kick-start bursts or contribute to them.
- With this score, we visualize the results with a heatmap (top 30 as an example for readability purposes).
- In normal situtations the heatmap would be very smooth and no spikes would be present. On the contrary, in our results we see the exact opposite. Very high activity in certain hours, and very low on others. 
- There is a distinct surge in activity between 5PM and 7PM for most high scoring users, while the rest of the hours are silent. This is a proof of coordination and "shift" work.

---------------------------------------------------------------------------------------
q10-4:
This file tackles and creates visualizations for user "roles" by analyzing activity.
- We divide the timeline into bursts and normal days, again from previous questions.
- We then calculate how many RTs each user did in each burst / normal period.
- We use the widely used metric lift to calculate the amplification score (lift = % RTs in bursts / % RTs in normal periods). For example a user with 10% of RTs in a burst gets a low score, while a user with 70% of RTs in bursts get a very high score.
- We create 2 important charts: 
    1. Most RTed authors, with the red bar showing the burst influence and blue the normal period influence.
    2. Roles plot: here, we create a visual map of all users with a color indicating system, with blue (<1.5) indicating normal behavior (consistent contribution during both bursts and normal days), gray (<3.5) mixed activity (1.5-3.5 more amplified in bursts) and red (>3.5 score) a certainly suspicious behavior which indicate the account is a bot that contributes mostly to bursts, or an amplifier, since a >3.5 makes their contribution to bursts very significant.