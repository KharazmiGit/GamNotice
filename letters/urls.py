from django.urls import path
from .views import  user_letter_counts

urlpatterns = [
    path('test/',user_letter_counts,name='test'),
]
