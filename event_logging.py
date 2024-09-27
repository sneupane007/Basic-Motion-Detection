import csv
import datetime

def log_motion_event():
    with open('motion_log.csv', mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([datetime.datetime.now()])
