from django.urls import path
from . import views

urlpatterns = [
    path('run/', views.scrape_letters,name='scrap_letter')
]