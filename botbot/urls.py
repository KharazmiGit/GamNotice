from django.urls import path
from . import views

urlpatterns = [
    path('run/', views.scrape_letters_for_user,name='scrap_letter'),
    path('loop-users/', views.all_gam_users,name='all_users')
]
