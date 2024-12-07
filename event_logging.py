import csv
from datetime import datetime, timedelta

def log_motion_event():
    with open('motion_log.csv', mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([datetime.datetime.now()])

def trim_csv(file_path, max_days=7):
    """
    Trim the CSV file to only keep rows within the past 'max_days' days.
    """
    # Load the CSV file
    try:
        df = pd.read_csv(file_path, header=None, names=['timestamp'])
        df['timestamp'] = pd.to_datetime(df['timestamp'], errors='coerce')
    except FileNotFoundError:
        print(f"File {file_path} not found. Creating a new file.")
        return pd.DataFrame(columns=['timestamp'])

    # Drop invalid timestamps
    df = df.dropna(subset=['timestamp'])

    # Calculate the cutoff date
    cutoff_date = datetime.now() - timedelta(days=max_days)

    # Keep only rows within the last 'max_days'
    df = df[df['timestamp'] >= cutoff_date]

    # Save the trimmed data back to the file
    df.to_csv(file_path, index=False, header=False)
    return df