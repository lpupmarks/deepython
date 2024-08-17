from flask import Flask
import requests
from bs4 import BeautifulSoup
import time
from threading import Thread

app = Flask(__name__)

# Global variable to store the latest content of the notifications page
latest_content = None

def fetch_notifications():
    global latest_content
    url = "https://lpupmarks.github.io/adre.html"

    try:
        # Send a GET request to fetch the page content
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for bad requests

        # Parse the HTML content using BeautifulSoup
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Extract the part of the page that contains the notifications.
        # Modify the selector based on the page structure. This is a placeholder.
        content = soup.find('div', class_='notifications-content') 

        # Check if the content has changed since the last fetch
        if latest_content is None:
            latest_content = content
        elif content != latest_content:
            latest_content = content
            send_alert()  # Trigger alert when changes are detected

    except Exception as e:
        print(f"Error fetching the page: {e}")

def send_alert():
    try:
        # Send POST request to notify about the detected change
        response = requests.post("https://ntfy.sh/philerts",
                                 data="Remote access to phils-laptop detected. Act right away.",
                                 headers={
                                     "Title": "Unauthorized access detected",
                                     "Priority": "urgent",
                                     "Tags": "warning,skull"
                                 })
        response.raise_for_status()  # Ensure no error occurred during the POST request
        print("Alert sent successfully")
    except Exception as e:
        print(f"Failed to send alert: {e}")

def start_monitoring():
    while True:
        fetch_notifications()
        time.sleep(3600)  # Sleep for one hour before fetching again

# Start the monitoring in a separate thread
monitoring_thread = Thread(target=start_monitoring)
monitoring_thread.daemon = True
monitoring_thread.start()

@app.route('/')
def home():
    return "Monitoring Notifications for Changes"

if __name__ == "__main__":
    app.run(debug=True, port=5000)
