import csv
import os
import pandas as pd
from datetime import datetime, timedelta
from config.settings import LOG_FILE

# Default log file path
DEFAULT_LOG_PATH = LOG_FILE

def log_motion_event(log_path=DEFAULT_LOG_PATH):
    """
    Log a motion event with the current timestamp.
    
    Args:
        log_path (str): Path to the CSV log file.
    """
    # Create directory if it doesn't exist
    os.makedirs(os.path.dirname(log_path), exist_ok=True)
    
    with open(log_path, mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([datetime.now()])

def trim_csv(file_path=DEFAULT_LOG_PATH, max_days=7):
    """
    Trim the CSV file to only keep rows within the past 'max_days' days.
    
    Args:
        file_path (str): Path to the CSV log file.
        max_days (int): Number of days to keep in the log file.
        
    Returns:
        DataFrame: The trimmed DataFrame.
    """
    # Load the CSV file
    try:
        df = pd.read_csv(file_path, header=None, names=['timestamp'])
        df['timestamp'] = pd.to_datetime(df['timestamp'], errors='coerce')
    except FileNotFoundError:
        print(f"File {file_path} not found. Creating a new file.")
        return pd.DataFrame(columns=['timestamp'])
    except Exception as e:
        print(f"Error reading log file: {e}")
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