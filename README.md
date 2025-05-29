# Motion Detection Dashboard

A Python and Flask-based application for real-time motion detection and visualization. I have tried to make the whole project readable and changable. I do plan to add intuitive comments in the future for better understanding. 

### Features

- Real-time motion detection using the device webcam(Need work on external webcam)
- Event logging with timestamps
- data visualization dashboard
- Adjustable time ranges (day, week, month, 3 months)
- Hour or minute-based aggregation of events

### Installation

1. Clone the repository:

2. Create and activate a virtual environment:

   ```
   python -m venv venv
   source venv/bin/activate
   ```

3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

### Usage

Run the application:

```
python program.py
```

Access the dashboard at http://localhost:5001

### Requirements

- Python 3.8 or higher
- Webcam (for motion detection)
- Flask and dependencies listed in requirements.txt

### Things left to do
- improve the detection algorithm
- for now I have copied all the css from else where. Plan to use tailwind for better and faster designs
- improve the data analysis part