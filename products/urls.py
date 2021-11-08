from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.products, name='products'),
    path('<int:product_id>/', views.product_view, name='product_view'),
    path('artists/', views.artists, name='artists'),
]
