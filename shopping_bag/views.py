from django.shortcuts import render, redirect
from django.conf import settings
from products.models import Product
from django.contrib import messages

# Create your views here.


def shopping_bag(request):
    ''' A view to return the users shopping bag page'''
    print("look here settings.FREE_DELIVERY_THRESHOLD> ", settings.FREE_DELIVERY_THRESHOLD)
    return render(request, 'shopping_bag.html')


def add_product_to_bag(request, item_id):
    ''' A view to add items to the shopping bag'''

    product = Product.objects.get(pk=item_id)

    quantity = int(request.POST.get('quantity'))
    redirect_url = request.POST.get('redirect_url')
    bag = request.session.get('bag', {})

    if item_id in list(bag.keys()):
        bag[item_id] += quantity
        messages.success(request, f'You have added {product.name} to your bag')
    else:
        bag[item_id] = quantity
        messages.success(request, f'You have added {product.name} to your bag')

    request.session['bag'] = bag
    return redirect(redirect_url)