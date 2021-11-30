from django.contrib import admin
from django.urls import path
from . import views
from .webhooks import webhook

urlpatterns = [
    path('', views.checkout, name='checkout'),
    path('order_success/<users_order_number>', views.order_complete, name='order_complete'),
    path('cache_checkout_data/', views.cache_checkout_data, name='cache_checkout_data'),
    path('webhook/', webhook, name='webhook'),
]
