import time, requests
from win10toast import ToastNotifier

API_URL = 'https://your.server.com/api/unread-letters/'
INTERVAL = 300  # seconds


def poll_and_notify(username, password):
    toaster = ToastNotifier()
    session = requests.Session()
    # Obtain auth token (if you use token auth) or login session
    resp = session.post('https://your.server.com/api/token/', data={
        'username': username, 'password': password
    })
    token = resp.json().get('access')
    headers = {'Authorization': f'Bearer {token}'}

    while True:
        r = session.get(API_URL, headers=headers, timeout=10)
        data = r.json().get('unread', [])
        count = len(data)
        if count:
            toaster.show_toast(
                "New Letters",
                f"You have {count} unread messages",
                duration=5,
                threaded=True
            )
        time.sleep(INTERVAL)


if __name__ == '__main__':
    poll_and_notify('testuser', 'testpassword')
