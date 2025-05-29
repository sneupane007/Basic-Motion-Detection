"""
API routes for the motion detection dashboard
"""
from flask import Blueprint, request, jsonify
import io
import base64
import pandas as pd
from datetime import datetime, timedelta
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

from config.settings import LOG_FILE


# Create a Blueprint for API routes
api_bp = Blueprint('api', __name__, url_prefix='/api')

def query_data(file_path, days_back=None):
    """
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


    return df

def plot_motion_data(df, group_by='hour'):
    """
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
    plt.figure(figsize=(6, 6))
    event_counts.plot(kind='bar', color='purple')
    plt.xlabel(xlabel)
    plt.ylabel("Number of Motion Events")
    plt.title(title)
    plt.xticks(rotation=0)
    plt.tight_layout()

    # Save the plot to a BytesIO object
    img = io.BytesIO()
    plt.savefig(img, format='png')
    plt.close()
    # Embed the result in the html output.
    img.seek(0)
    plot_image = base64.b64encode(img.read()).decode('utf-8')
    
    return plot_image

@api_bp.route('/data', methods=['GET'])
def get_data():
    """
    fetch API end motion data for a specified range.
    """
    range_type = request.args.get('range', default = 'day')  # Get range from query params
    group_by = request.args.get('group_by', default = 'hour')  # 'hour' or 'minute'

    print(f"Range: {range_type}, Group By: {group_by}")
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
        
    # Send the image file to static/js/main.js
    return jsonify({"plot": plot_image}) 

