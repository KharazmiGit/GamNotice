from django.db.models import Count, Q
from django.http import JsonResponse
import requests

from botbot.models import GamUser


def user_letter_counts(request):
    # Annotate only unsent letters per user
    user_data = GamUser.objects.annotate(
        letter_count=Count('user_letter', filter=Q(user_letter__sent=False))
    ).filter(
        letter_count__gt=0
    )

    user_info = []
    for user in user_data:
        user_info.append({
            "username": user.username,
            "letter_count": user.letter_count,
            "desktop_ip": user.desktop_ip
        })

    # Send notifications
    for user in user_info:
        try:
            response = requests.post(
                f"http://{user['desktop_ip']}:5000/notify",
                json={
                    'letter_count': user['letter_count'],
                    'username': user['username']
                },
                timeout=5
            )
            response.raise_for_status()
        except requests.RequestException as e:
            print(f"Failed to send notification to {user['username']}: {e}")

    return JsonResponse(user_info, safe=False)
