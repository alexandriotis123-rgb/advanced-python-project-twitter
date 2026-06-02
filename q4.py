import pandas as pd
import matplotlib.pyplot as plt
from q1 import process_mati_data
import os

input_file = "data/mati_q1_relevant.csv"
if os.path.exists(input_file):
    df = pd.read_csv(input_file)
else:
    df = process_mati_data("mati.csv")

df['created_at'] = pd.to_datetime(df['created_at'], errors='coerce')
df = df.dropna(subset=['created_at'])
df['hour'] = df['created_at'].dt.hour
df['date'] = df['created_at'].dt.date

# average
hourly_counts = df.groupby(['date', 'hour']).size().reset_index(name='count')
avg_activity = hourly_counts.groupby('hour')['count'].mean().reset_index()

# fill missing hours
all_hours = pd.DataFrame({'hour': range(24)})
avg_activity = pd.merge(all_hours, avg_activity, on='hour', how='left').fillna(0)
avg_activity = avg_activity.sort_values('hour')

plt.style.use('seaborn-v0_8-muted') 
fig, ax = plt.subplots(figsize=(12, 6))
ax.bar(avg_activity['hour'], avg_activity['count'], color='royalblue', alpha=0.8)
ax.set_title('Average Tweet Volume by Hour of Day', fontsize=14)
ax.set_xlabel('Hour of Day')
ax.set_ylabel('Average Number of Tweets')
ax.grid(axis='y', linestyle='--', alpha=0.6)
ax.tick_params(axis='both', which='major', labelsize=10)
ax.set_xticks(range(0, 24))

plt.tight_layout()
plt.savefig('plots/q4_time_analysis.png')
plt.show()