from flask import Flask, request
from threading import Thread, Event
import queue
from plyer import notification
import os
import requests
import logging

# Configure logging
logging.basicConfig(
    filename='notifier.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

app = Flask(__name__)
notification_queue = queue.Queue()
stop_flag = Event()


def show_notification(msg):
    """Displays a desktop notification using Plyer."""
    notification.notify(
        title="پیام‌رسان خوارزمی",
        message=msg,
        app_name="پیام‌رسان خوارزمی",
        timeout=86400
    )


def notification_worker():
    """Continuously processes notifications from the queue."""
    while not stop_flag.is_set():
        msg = notification_queue.get()
        show_notification(msg)
        notification_queue.task_done()


# Creating and starting the notification worker thread
notification_thread = Thread(target=notification_worker, daemon=True, name="NotificationWorker")
notification_thread.start()


@app.route('/notify', methods=['POST'])
def notify():
    """Handles incoming notification requests."""
    try:
        data = request.get_json()
        if not data or 'username' not in data or 'letter_count' not in data:
            return {"status": "error", "message": "Invalid request"}, 400

        message = f"کاربر {data['username']}:\nشما {data['letter_count']} نامهٔ خوانده‌نشده دارید!"
        notification_queue.put(message)
        return {"status": "received"}
    except Exception as e:
        return {"status": "error", "message": str(e)}, 500


@app.route('/shutdown', methods=['POST'])
def shutdown():
    """Gracefully stops the notification worker thread."""
    stop_flag.set()
    notification_thread.join()
    return {"status": "shutdown successful"}


if __name__ == '__main__':
    logging.info("Starting application...")
    # Send test notification on startup
    notification_queue.put("سرویس نوتیفیکیشن فعال شد! (Notification service started)")
    app.run(host='0.0.0.0', port=5000)