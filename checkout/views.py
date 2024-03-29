from django.shortcuts import (render, redirect, reverse, get_object_or_404,
                              HttpResponseRedirect, HttpResponse)
from django.views.decorators.http import require_POST
from .forms import UsersOrderForm, Order
from django.contrib import messages
from django.shortcuts import render, redirect, reverse
from django.conf import settings
import stripe
from shopping_bag.context import bag_contents
from products.models import Product
from .models import Order, OrderItem
import json
from profiles.forms import UsersProfileForm
from profiles.models import UserProfile
# Create your views here.


@require_POST
def cache_checkout_data(request):
    try:
        pid = request.POST.get('client_secret').split('_secret')[0]
        stripe.api_key = settings.STRIPE_PRIVATE_KEY
        stripe.PaymentIntent.modify(pid, metadata={
            'bag': json.dumps(request.session.get('bag', {})),
            'save_info': request.POST.get('save_info'),
            'username': request.user,
        })
        return HttpResponse(status=200)
    except Exception as e:
        messages.error(request, 'Sorry cannot process right now')
        return HttpResponse(content=e, status=400)


def checkout(request):
    stripe_public_key = settings.STRIPE_PUBLIC_KEY
    stripe_secret_key = settings.STRIPE_PRIVATE_KEY

    if request.method == 'POST':
        cyberplates_for_checkout = request.session.get('bag', {})
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
            order = order_form.save(commit=False)
            pid = request.POST.get('client_secret').split('_secret')[0]
            order.stripe_pid = pid
            order.original_bag = json.dumps(cyberplates_for_checkout)
            order.save()
            for item_id, item_data in cyberplates_for_checkout.items():
                product = Product.objects.get(id=item_id)
                if isinstance(item_data, int):
                    order_line_item = OrderItem(
                        order_item=order,
                        product=product,
                        quantity=item_data,
                    )
                    order_line_item.save()
            return(HttpResponseRedirect(
                reverse('order_complete', args=[order.users_order_number])))
        else:
            messages.error(request, 'Sorry there was an issue. \
                Please check your information.')
    else:
        cyberplates_for_checkout = request.session.get('bag', {})
        if not cyberplates_for_checkout:
            messages.error(request, "You don't have any items")
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
            'client_secret': intent.client_secret,
        }

        return render(request, template, context)


def order_complete(request, users_order_number):
    save_info = request.session.get('save_info')
    order = get_object_or_404(Order, users_order_number=users_order_number)
    cyberplates_for_checkout = request.session.get('bag', {})
    messages.success(request, f'Your order is successful! \
        Your order number is {users_order_number}. \
            Thank you {order.first_name}.')

    if request.user.is_authenticated:
        profile = UserProfile.objects.get(user=request.user)
        '''
        Attach the user's profile to the order
        '''
        order.user_profile = profile
        order.save()

        if save_info:
            profile_data = {
                'def_first_name': order.first_name,
                'def_last_name': order.last_name,
                'def_email ': order.email,
                'def_phone': order.phone,
                'def_street ': order.street,
                'def_town ': order.town,
            }
            user_profile_form = user_profile_form(
                profile_data, instance=profile)
            if user_profile_form.is_valid():
                user_profile_form.save()

    current_bag = bag_contents(request)
    total = current_bag['grand_total']
    if 'bag' in request.session:
        del request.session['bag']

    template = 'checkout/order_success.html'
    context = {
        'order': order,
        'total': total
    }
    return render(request, template, context)
