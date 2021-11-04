from django.shortcuts import render
from .models import Product

# Create your views here.


def view_products(request):
    ''' A view to return the products page'''
    all_products = Product.objects.all()
    context = {
        'all_products': all_products
    }

    return render(request, 'products/products.html', context)
