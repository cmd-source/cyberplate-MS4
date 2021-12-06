from django import forms
from .models import Product_Category, Product, Artist

class ProductForm(forms.ModelForm):

    class Meta:
        model = Product
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        super().__init__(*args, **kwargs)
        placeholders = {
            'product_category': 'product_category',
            'artist': 'artist',
            'name': 'name',
            'description': 'description',
            'price': 'price',
            'image_url': 'image_url',
            'image': 'image',
            'product_key': 'product_key',
            }
