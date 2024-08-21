from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('data/', views.getData),
    path('add/', views.postData),
    path('lastest/', views.getLastetData),
]