from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.checkout, name='checkout'),
    path('order_success/<users_order_number>', views.order_complete, name='order_complete'),
]
