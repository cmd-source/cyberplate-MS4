from django.shortcuts import render
from .forms import UsersOrderForm, Order
from django.contrib import messages
from django.shortcuts import render, redirect, reverse
from django.conf import settings
import stripe
from shopping_bag.context import bag_contents
# Create your views here.


def checkout(request):
    public_key = settings.STRIPE_PUBLIC_KEY
    secret_key = settings.STRIPE_PRIVATE_KEY

    cyberplates_for_checkout = request.session.get('bag', {})
    if not cyberplates_for_checkout:
        return redirect(reverse('products'))

    current_bag = bag_contents(request)
    total = current_bag['grand_total']
    stripe_charge = round(total*100)
    stripe.api_key = secret_key
    intent = stripe.PaymentIntent.create(
        amount=stripe_charge,
        currency=settings.STRIPE_CURRENCY
    )
    print(intent)
    users_order = UsersOrderForm()
    template = 'checkout/checkout.html'
    context = {
        'users_order': users_order,
        'stripe_public_key': 'pk_test_51K01qvDRUt70JrpHQW1Dccpt6WN7MBu8jkc8r2ruCcmWUXIxleZNTBloQDR9kFqOiJNOfyALVRgF5ADEuXxWQglf00M4aE8CRv',
        'stripe_secret_key': 'test client secret',
    }


    return render(request, template, context)
