from django.shortcuts import render, get_object_or_404
from django.contrib import messages
from django.db.models import Q
from .models import Product

# Create your views here.


def products(request):
    ''' A view to return the products page'''

    all_products = Product.objects.all()
    search = None

    if request.GET:
        if 'search' in request.GET:
            search = request.GET['search']
        else:
            messages.error(request, 'This is not a vaild search')

        searched_query = Q(name__icontains=search) | Q(description__icontains=search) 
        all_products = all_products.filter(searched_query)

    context = {
        'all_products': all_products,
        'search': search
    }

    return render(request, 'products/products.html', context)


def product_view(request, product_id):
    ''' Opens a more detailed view of the Cyberplate selected on'''
    selected_product = get_object_or_404(Product, pk=product_id)
    context = {
        'selected_product': selected_product
    }

    return render(request, 'products/product_view.html', context)
