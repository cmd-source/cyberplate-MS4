from django.db import models
import uuid
from django.db.models import Sum
from products.models import Product


class Order(models.Model):
    users_order_number = models.CharField(max_length=50, null=False, editable=False)
    first_name = models.CharField(max_length=50, null=False, blank=False)
    last_name = models.CharField(max_length=50, null=False, blank=False)
    email = models.EmailField(max_length=50, null=False, blank=False)
    phone = models.CharField(max_length=50, null=False, blank=False)
    street = models.CharField(max_length=100, null=False, blank=False)
    town = models.CharField(max_length=100, null=False, blank=True)
    country = models.CharField(max_length=100, null=False, blank=True)
    order_date = models.DateTimeField(auto_now_add=True)
    order_total = models.DecimalField(max_digits=8, decimal_places=2, null=False, default=0)

    def order_number(self):

        return uuid.uuid4().hex.upper()

    def save(self, *args, **kwargs):

        if not self.users_order_number:
            self.users_order_number = self.order_number()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.users_order_number


class OrderItem(models.Model):
    order_item = models.ForeignKey(Order, null=False, blank=False, on_delete=models.CASCADE, related_name='lineitems')
    product = models.ForeignKey(Product, null=False, blank=False, on_delete=models.CASCADE)
    quantity = models.IntegerField(null=False, blank=False, default=0)
    lineitem_total = models.DecimalField(max_digits=6, decimal_places=2, null= False, blank=False)

    def save(self, *args, **kwargs):

        self.lineitem_total = self.product.price * self.quantity
        super().save(*args, **kwargs)
