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
        'users_order': users_order,
        'stripe_public_key': 'pk_test_51K01qvDRUt70JrpHQW1Dccpt6WN7MBu8jkc8r2ruCcmWUXIxleZNTBloQDR9kFqOiJNOfyALVRgF5ADEuXxWQglf00M4aE8CRv',
        'stripe_secret_key': 'test client secret',
    }


    return render(request, template, context)
