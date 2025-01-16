# Motion Detection Dashboard

A web application built with Flask and Tailwind CSS to log, analyze, and visualize motion events dynamically. This application provides an interactive dashboard to monitor and explore motion data.

## Features

- **Motion Event Logging**: Captures motion events with timestamps and stores them in a CSV file.
- **Data Visualization**: Displays motion events using dynamic bar charts grouped by hour or minute.
- **Custom Time Ranges**: Filter and view data for the last day, week, month, or three months.
- **Interactive Dashboard**: User-friendly interface built with Tailwind CSS.
- **API Access**: Fetch motion event data and visualizations programmatically.

## Tech Stack

- **Backend**: Flask
- **Frontend**: Tailwind CSS
- **Visualization**: Matplotlib, Plotly
- **Data Storage**: CSV files (optionally SQLite for scalability which I am working with)

## Installation

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/your-username/motion-detection-dashboard.git
   cd motion-detection-dashboard
   ```

2. **Set Up a Virtual Environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate   # On Windows: venv\Scripts\activate
   ```

3. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the Application**:
   ```bash
   python app.py
   ```

5. **Access the Dashboard**:
   Open [http://127.0.0.1:5000](http://127.0.0.1:5000) in your browser.

## Usage

1. **Log Motion Events**:
   - Motion events are logged into a file (`motion_log.csv`) automatically.
   
2. **Visualize Data**:
   - Use the dashboard to select a time range and grouping criteria (hour or minute).
   - View dynamically generated motion event plots.

3. **API Endpoints**:
   - `/api/data?range=week&group_by=hour`: Fetch motion data for the past week grouped by hour.
   - Replace `range` and `group_by` values as needed (`day`, `month`, `minute`, etc.).

## Future Improvements

- Add real-time data visualization with WebSockets.
- Integrate with a database for enhanced scalability.
- Provide support for additional visualization types like scatter plots or heatmaps.

