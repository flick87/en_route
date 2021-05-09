
from django.contrib import admin
from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name='tracker-home'),
    path('new_customer', views.create_customer, name='tracker-new_customer'),
    path('new_ticket', views.create_ticket, name='tracker-new_ticket'),
    path('view_tickets', views.view_tickets, name='tracker-view_tickets'),
    path('view_customers', views.view_customers, name='tracker-view_customers'),
    path('equipment', views.equipment, name='tracker-equipment'),
]
