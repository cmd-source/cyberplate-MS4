
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from .models import OrderItem
'''
These signals were taken directly from the
Code Institutes walkalong project Boutique Ado
'''


@receiver(post_save, sender=OrderItem)
def update_on_save(sender, instance, created, **kwargs):
    """
    Update order total on lineitem update/create
    """
    instance.order_item.update_total()


@receiver(post_delete, sender=OrderItem)
def update_on_delete(sender, instance, **kwargs):
    """
    Update order total on lineitem delete
    """
    instance.order_item.update_total()
