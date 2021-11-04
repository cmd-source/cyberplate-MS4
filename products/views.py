from django.shortcuts import render, get_object_or_404
from .models import Product

# Create your views here.


def products(request):
    ''' A view to return the products page'''
    all_products = Product.objects.all()
    context = {
        'all_products': all_products
    }

    return render(request, 'products/products.html', context)


def product_view(request, product_id):
    ''' Opens a more detailed view of the Cyberplate selected on'''
    selected_product = get_object_or_404(Product, pk=product_id)
    context = {
        'selected_product': selected_product
    }

    return render(request, 'products/product_view.html', context)
