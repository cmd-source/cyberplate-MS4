from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('shopping_bag', views.shopping_bag, name='shopping_bag'),
]