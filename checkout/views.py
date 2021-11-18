from django.shortcuts import render
from .forms import UsersOrderForm, Order
from django.contrib import messages
from django.shortcuts import render, redirect, reverse
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

    return render(request, template, context)
