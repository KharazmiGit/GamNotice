from django.urls import path
from . import views

urlpatterns = [
    path('run/', views.scrape_all_users,name='do-it'),
]
