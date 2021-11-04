from django.contrib import admin
from .models import Product, Product_Category, Artist

# Register your models here.
admin.site.register(Product_Category)
admin.site.register(Artist)
admin.site.register(Product)
