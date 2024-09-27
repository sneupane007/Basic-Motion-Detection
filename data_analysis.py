import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv('motion_log.csv', header=None, names=['timestamp'])
df['timestamp'] = pd.to_datetime(df['timestamp'])

df['hour'] = df['timestamp'].dt.hour
event_counts = df.groupby('hour').size()


event_counts.plot(kind='bar')
plt.xlabel('Hour of Day')
plt.ylabel('Number of Motion Events')
plt.title('Motion Events by Hour')
plt.show()
