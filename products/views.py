from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib import messages
from django.db.models import Q
from .models import Product, Artist, Product_Category


# Create your views here.
 

def products(request):
    ''' A view to return the products page'''

    all_products = Product.objects.all()
    search = None
    categories = None

    if request.GET:
        if 'category_selected' in request.GET:
            categories = request.GET['category_selected']
            all_products = Product.objects.filter(product_category=categories)
            categories = Product.objects.filter(name=categories)

        if 'search' in request.GET:
            search = request.GET['search']
            if not search:
                messages.error(request, 'This is not a vaild search')
                return redirect(reverse('products'))

            searched_query = Q(name__icontains=search) | Q(description__icontains=search) 
            all_products = all_products.filter(searched_query)

    context = {
        'all_products': all_products,
        'search': search,
        'current_categories': categories
    }

    return render(request, 'products/products.html', context)


def product_view(request, product_id):
    ''' Opens a more detailed view of the Cyberplate selected on'''
    print(f'Product_id from product_view: {product_id}')
    selected_product = get_object_or_404(Product, pk=product_id)
    context = {
        'selected_product': selected_product
    }
    # print(product_id)

    return render(request, 'products/product_view.html', context)


def artists(request):
    ''' A view to return the artists page'''

    all_artists = Artist.objects.all()
    print(f'All artists: {all_artists}')
    context = {
        'all_artists': all_artists,
    }

    return render(request, 'products/artists.html', context)



def artist_view(request, artist_id):
    '''Opens a more detailed view of the Cyberplate selected on'''
    selected_artist = get_object_or_404(Artist, pk=artist_id)
    print('selected_artist >>',selected_artist)
    artists_products = Product.objects.all().filter(artist=selected_artist)
    print('artists_products >>',artists_products)

    context = {
        'selected_artist': selected_artist,
        'artists_products': artists_products
    }

    return render(request, 'products/artist_view.html', context)
