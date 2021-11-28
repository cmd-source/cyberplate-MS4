from django.shortcuts import render, redirect, reverse, get_object_or_404
from .forms import UsersOrderForm, Order
from django.contrib import messages
from django.shortcuts import render, redirect, reverse
from django.conf import settings
import stripe
from shopping_bag.context import bag_contents
from products.models import Product
from .models import Order, OrderItem
# Create your views here.


def checkout(request):
    stripe_public_key = settings.STRIPE_PUBLIC_KEY
    stripe_secret_key = settings.STRIPE_PRIVATE_KEY

    print(request.method == 'POST')
    if request.method == 'POST':
        cyberplates_for_checkout = request.session.get('bag', {})
        print('Printing if POST', cyberplates_for_checkout)
        form_data = {
            'first_name': request.POST['first_name'],
            'last_name': request.POST['last_name'],
            'email': request.POST['email'],
            'phone': request.POST['phone'],
            'street': request.POST['street'],
            'town': request.POST['town'],
        }
        order_form = UsersOrderForm(form_data)
        if order_form.is_valid():
            order = order_form.save()
            for item_id, item_data in cyberplates_for_checkout.items():
                product = Product.objects.get(id=item_id)
                print('Item ID >> ', item_id)
                print('Item DATA >> ', item_data)
                print('Item PRODUCT >> ', product)
                if isinstance(item_data, int):
                    order_line_item = OrderItem(
                        order_item=order,
                        product=product,
                        quantity=item_data,
                    )
                    order_line_item.save()
                    print('Order line item >> ', order_line_item)
            return(reverse('order_complete', args=[order.users_order_number]))
    else:
        cyberplates_for_checkout = request.session.get('bag', {})
        print('Printing if ELSE',cyberplates_for_checkout)
        if not cyberplates_for_checkout:
            return redirect(reverse('products'))

        current_bag = bag_contents(request)
        total = current_bag['grand_total']
        stripe_charge = round(total*100)
        stripe.api_key = stripe_secret_key
        intent = stripe.PaymentIntent.create(
            amount=stripe_charge,
            currency=settings.STRIPE_CURRENCY
        )
        users_order = UsersOrderForm()
        template = 'checkout/checkout.html'
        context = {
            'users_order': users_order,
            'stripe_public_key': stripe_public_key,
            'stripe_secret_key': intent.client_secret,
        }

        return render(request, template, context)


def order_complete(request, users_order_number):
    order = get_object_or_404(Order, users_order_number=users_order_number)

    if 'bag' in request.session:
        del request.session['bag']

    template = 'checkout/order_success.html'
    context = {
        'order': order
    }

    return render(request, render, template)
