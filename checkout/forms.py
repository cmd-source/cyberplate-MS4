from django import forms
from .models import Order


class UsersOrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ('first_name', 'last_name', 'email',
                  'phone', 'street', 'town', 'country',)

# Taken and altered from the Code Institutes walkthrough Project Boutique Ado
        def __init__(self, *args, **kwargs):
            """
            Add placeholders and classes, remove auto-generated
            labels and set autofocus on first field
            """
            super().__init__(*args, **kwargs)
            placeholders = {
                'first_name': 'first_name',
                'last_name': 'last_name',
                'email': 'email',
                'phone': 'phone',
                'street': 'street',
                'town': 'town',
                'country': 'country',
            }
