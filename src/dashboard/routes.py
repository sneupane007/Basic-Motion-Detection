"""
Dashboard routes for the motion detection application
"""
from flask import Blueprint, render_template

# Create a Blueprint for dashboard routes
dashboard_bp = Blueprint('dashboard', __name__)

@dashboard_bp.route('/')
def index():
    """
    Render the dashboard UI.
    """
    return render_template('index.html')

@dashboard_bp.route('/about')
def about():
    """
    Render the about page.
    """
    return render_template('about.html')

@dashboard_bp.route('/settings')
def settings():
    """
    Render the settings page.
    """
    return render_template('settings.html') 