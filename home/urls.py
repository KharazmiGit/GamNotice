from django.urls import path
from . import views

urlpatterns = [
    path('', views.IndexClassBaseView.as_view(), name='index-page'),
]
