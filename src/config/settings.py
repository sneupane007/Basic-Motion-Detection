"""
Application configuration settings
"""
import os
from pathlib import Path

# Base directory of the project
BASE_DIR = Path(__file__).resolve().parent.parent.parent

# Data storage
DATA_DIR = os.path.join(BASE_DIR, 'data')
LOG_FILE = os.path.join(DATA_DIR, 'motion_log.csv')

# Flask settings
DEBUG = True
HOST = '0.0.0.0'
PORT = 5000

# Motion detection settings
MOTION_THRESHOLD = 20
MIN_CONTOUR_AREA = 1000
DILATE_ITERATIONS = 3

# Data retention settings
MAX_LOG_DAYS = 30

# Ensure directories exist
os.makedirs(DATA_DIR, exist_ok=True) 