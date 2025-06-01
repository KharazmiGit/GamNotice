from flask import Flask, request
from threading import Thread
import queue
from plyer import notification

app = Flask(__name__)
notification_queue = queue.Queue()


def show_notification(msg):
    notification.notify(
        title="Gam Notifier",
        message=msg,
        app_name="Gam Service",
        timeout=20  # Notification disappears after 10 sec
    )


def notification_worker():
    while True:
        msg = notification_queue.get()
        show_notification(msg)
        notification_queue.task_done()


notification_thread = Thread(target=notification_worker, daemon=True)
notification_thread.start()


@app.route('/notify', methods=['POST'])
def notify():
    data = request.get_json()
    message = f"New letter from {data['sender']}, ID: {data['letter_id']}"
    notification_queue.put(message)
    return {"status": "received"}


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
