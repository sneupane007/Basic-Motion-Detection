from flask import Flask, request, jsonify, render_template, send_file
import pandas as pd
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import io

# Filepath for motion_log.csv
FILE_PATH = 'motion_log.csv'

app = Flask(__name__)


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

def query_data(file_path, days_back=None):
    """
    Query data from the CSV file for the past 'days_back' days.
    """
    # Load the CSV file
    try:
        df = pd.read_csv(file_path, header=None, names=['timestamp'])
        df['timestamp'] = pd.to_datetime(df['timestamp'], errors='coerce')
    except FileNotFoundError:
        print(f"No data available. File {file_path} does not exist.")
        return pd.DataFrame(columns=['timestamp'])

    # Drop invalid timestamps
    df = df.dropna(subset=['timestamp'])

    # If days_back is specified, filter data for that range
    if days_back is not None:
        cutoff_date = datetime.now() - timedelta(days=days_back)
        df = df[df['timestamp'] >= cutoff_date]

    return df

def plot_motion_data(df, group_by='hour'):
    """
    Plot motion data grouped by 'hour' or 'minute'.
    """
    if df.empty:
        print("No data available to plot.")
        return

    if group_by == 'hour':
        df['hour'] = df['timestamp'].dt.hour
        event_counts = df.groupby('hour').size()
        title = "Motion Events by Hour"
        xlabel = "Hour of Day"
    elif group_by == 'minute':
        df['minute'] = df['timestamp'].dt.minute
        event_counts = df.groupby('minute').size()
        title = "Motion Events by Minute (Aggregated Over All Hours)"
        xlabel = "Minute of Hour"
    else:
        print(f"Invalid group_by value: {group_by}")
        return

    # Plotting
    plt.figure(figsize=(12, 6))
    event_counts.plot(kind='bar', color='purple')
    plt.xlabel(xlabel)
    plt.ylabel("Number of Motion Events")
    plt.title(title)
    plt.xticks(rotation=0)
    plt.tight_layout()
    plt.show()



@app.route('/api/data', methods=['GET'])
def get_data():
    """
    API endpoint to fetch motion data for a specified range.
    """
    range_type = request.args.get('range', 'week')  # Get range from query params
    group_by = request.args.get('group_by', 'hour')  # 'hour' or 'minute'

    # Map range_type to days_back
    range_map = {
        'day': 1,
        'week': 7,
        'month': 30,
        'three_months': 90
    }

    days_back = range_map.get(range_type)
    if days_back is None:
        return jsonify({"error": "Invalid range type"}), 400

    # Trim the CSV file to keep only recent data (e.g., past 90 days)
    # Adjust max_days as needed
    trim_csv(FILE_PATH, max_days=90)

    # Query data
    df = query_data(FILE_PATH, days_back)

    # Generate plot
    plot_image = plot_motion_data(df, group_by=group_by)
    if plot_image is None:
        return jsonify({"error": "No data available for the selected range"}), 404

    # Send the image file
    return send_file(plot_image, mimetype='image/png')




@app.route('/')
def index():
    """
    Render the dashboard UI.
    """
    return render_template('/index.html')

if __name__ == '__main__':
    app.run(debug=True)
