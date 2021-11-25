from django.shortcuts import render
from .forms import UsersOrderForm, Order
from django.contrib import messages
from django.shortcuts import render, redirect, reverse
from django.conf import settings
# Create your views here.


def checkout(request):
    cyberplates_for_checkout = request.session.get('bag', {})
    if not cyberplates_for_checkout:
        return redirect(reverse('products'))

    users_order = UsersOrderForm()
    template = 'checkout/checkout.html'
    context = {
        'users_order': users_order
    }

    print("look here> ", settings.FREE_DELIVERY_THRESHOLD)

    return render(request, template, context)
