"""
API routes for the motion detection dashboard
"""
from flask import Blueprint, request, jsonify
import io
import base64
import pandas as pd
from datetime import datetime, timedelta
import matplotlib.pyplot as plt

from src.config.settings import LOG_FILE
from src.utils.event_logger import trim_csv

# Create a Blueprint for API routes
api_bp = Blueprint('api', __name__, url_prefix='/api')

def query_data(file_path, days_back=None):
    """
    Query data from the CSV file for the past 'days_back' days.
    
    Args:
        file_path (str): Path to the CSV log file.
        days_back (int): Number of days to query back.
        
    Returns:
        DataFrame: The filtered DataFrame.
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
    
    Args:
        df (DataFrame): The DataFrame containing motion timestamps.
        group_by (str): How to group the data ('hour' or 'minute').
        
    Returns:
        str: Base64 encoded image data.
    """
    if df.empty:
        print("No data available to plot.")
        return None

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
        return None

    # Plotting
    plt.figure(figsize=(12, 6))
    event_counts.plot(kind='bar', color='purple')
    plt.xlabel(xlabel)
    plt.ylabel("Number of Motion Events")
    plt.title(title)
    plt.xticks(rotation=0)
    plt.tight_layout()

    # Save the plot to a BytesIO object
    img = io.BytesIO()
    plt.savefig(img, format='png')
    
    # Embed the result in the html output.
    fig_data = base64.b64encode(img.getbuffer()).decode("ascii")

    return fig_data

@api_bp.route('/data', methods=['GET'])
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

    # Query data
    df = query_data(LOG_FILE, days_back)

    # Generate plot
    plot_image = plot_motion_data(df, group_by=group_by)
    if plot_image is None:
        return jsonify({"error": "No data available for the selected range"}), 404
        
    # Send the image file
    return jsonify({"plot": plot_image}) 