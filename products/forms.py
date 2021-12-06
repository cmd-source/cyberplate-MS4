from django import forms
from .models import Product_Category, Product, Artist

class ProductForm(forms.ModelForm):

    class Meta:
        model = Product
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args,**kwargs)

        categories = Product_Category.objects.all()
        #friendly_names = [(c.id, c.get_friendly_name()) for c in categories]

        #self.fields['category'].choices = friendly_names

        creator = Artist.objects.all()
        #creator_friendly_names = [(a.id, a.get_friendly_name()) for a in creator]