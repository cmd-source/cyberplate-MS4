from django.shortcuts import render, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import UserProfile
from .forms import UsersProfileForm
from checkout.models import Order
from django.contrib.admin.views.decorators import staff_member_required

# Create your views here.
@login_required
def profile(request):
    """ Display the user's profile. """
    profile = get_object_or_404(UserProfile, user=request.user)

    if request.method == 'POST':
        form = UsersProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully')
        else:
            messages.error(request, 'Profile was not updated successfully!')
    form = UsersProfileForm(instance=profile)
    orders = profile.orders.all()

    template = 'profiles/profile.html'
    context = {
        'form': form,
        'orders': orders,
        'on_profile_page': True
    }

    return render(request, template, context)
    


def order_history(request, users_order_number):
    order = get_object_or_404(Order, users_order_number=users_order_number)

    messages.info(request, (f'This is a previous order'))

    template ='checkout/order_success.html'
    context = {
        'order': order,
        'from_profile': True,
    }

    return render(request, template, context)