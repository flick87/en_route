
from django.contrib import admin
from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name='tracker-home'),
    path('new_customer', views.create_customer, name='tracker-new_customer'),
]
