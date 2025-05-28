from django.urls import path
from .views import UnreadLettersView

urlpatterns = [
    path('api/unread-letters/', UnreadLettersView.as_view(), name='unread_letters'),
]
