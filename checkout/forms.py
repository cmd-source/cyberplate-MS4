from django import forms
from models import Order

class UsersOrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ('users_order_number','first_name', 'last_name', 'email', 'phone' , 'street', 'town', 'country',) 


        # Taken directly from the Code Institutes walkthrough Project Boutique Ado
        def __init__(self, *args, **kwargs):
            """
            Add placeholders and classes, remove auto-generated
            labels and set autofocus on first field
            """
            super().__init__(*args, **kwargs)
            placeholders = {
                'full_name': 'Full Name',
                'email': 'Email Address',
                'phone_number': 'Phone Number',
                'country': 'Country',
                'postcode': 'Postal Code',
                'town_or_city': 'Town or City',
                'street_address1': 'Street Address 1',
                'street_address2': 'Street Address 2',
                'county': 'County',
            }