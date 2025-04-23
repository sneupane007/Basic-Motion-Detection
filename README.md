# Motion Detection Dashboard

A Python and Flask-based application for real-time motion detection and visualization.

## Features

- Real-time motion detection using your webcam
- Event logging with precise timestamps
- Interactive data visualization dashboard
- Adjustable time ranges (day, week, month, 3 months)
- Hour or minute-based aggregation of events

## Project Structure

```
├── data/               # Directory for storing motion log data
├── src/                # Source code
│   ├── api/            # API endpoints
│   ├── config/         # Configuration settings
│   ├── core/           # Core application logic
│   ├── dashboard/      # Dashboard routes
│   ├── motion_detection/  # Motion detection logic
│   ├── utils/          # Utility functions
│   └── app.py          # Main application initialization
├── static/             # Static assets
│   ├── css/            # CSS stylesheets
│   ├── js/             # JavaScript files
│   └── img/            # Images
├── templates/          # HTML templates
│   ├── index.html      # Dashboard template
│   ├── about.html      # About page template
│   └── settings.html   # Settings page template
├── run.py              # Main entry point
└── requirements.txt    # Python dependencies
```

## Installation

1. Clone the repository:

   ```
   git clone <repository-url>
   cd motion-detection-dashboard
   ```

2. Create and activate a virtual environment:

   ```
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

## Usage

Run the application:

```
python run.py --mode all
```

Available modes:

- `web`: Run only the web dashboard
- `detection`: Run only the motion detection
- `all`: Run both the dashboard and motion detection (default)

Access the dashboard at http://localhost:5000

## Requirements

- Python 3.8 or higher
- Webcam (for motion detection)
- Flask and dependencies listed in requirements.txt

## License

This project is licensed under the MIT License - see the LICENSE file for details.
