from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('shopping_bag', views.shopping_bag, name='shopping_bag'),
    path('add/<item_id>', views.add_product_to_bag, name='add_product_to_bag'),
    path('adjust/<item_id>/', views.adjust_bag, name='adjust_bag'),
    path('remove/<item_id>/', views.remove, name='remove')
]