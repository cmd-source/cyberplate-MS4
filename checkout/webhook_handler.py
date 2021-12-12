from django.http import HttpResponse
from .models import Order, OrderItem
from products.models import Product

import json
import time


class StripeWH_Handler:
    """Handle Stripe webhooks"""

    def __init__(self, request):
        self.request = request
        print("WEBHOOK RAN:")

    def handle_event(self, event):
        """
        Handle a generic event from Stripe
        """
        return HttpResponse(
            content=f'Unhandled webhook received: {event["type"]}',
            status=200)

    def handle_payment_intent_succeeded(self, event):
        """
        Handle the payment_intent.succeeded webhook from Stripe
        """
        intent = event.data.object
        pid = intent.id
        bag = intent.metadata.bag
        save_info = intent.metadata.save_info

        billing_details = intent.charges.data[0].billing_details
        shipping_details = intent.shipping
        grand_total = round(intent.charges.data[0].amount / 100, 2)

        for field, value in shipping_details.address.items():
            if value == "":
                shipping_details.address[field] = None

        order_exists = False
        attempt = 1
        while attempt <= 5:
            try:
                order = Order.objects.get(
                    first_name__iexact=shipping_details.name,
                    street__iexact=shipping_details.address.line1,
                    town__iexact=shipping_details.address.city,
                    original_bag=bag,
                    stripe_pid=pid,
                )
                order_exits = True
                break
            except Order.DoesNotExist:
                attempt += 1
                time.sleep(1)
        if order_exists:
            print('The order exists >> ', order_exists)
            return HttpResponse(
                content=f'The payment has succeeded webhook received: {event["type"]} | Success order in database',
                status=200)
        else:
            order = None
            try:
                print('Order doesnt Try statment >> ', order)
                order = Order.objects.create(
                        first_name=shipping_details.name,
                        street=shipping_details.address.line1,
                        town=shipping_details.address.city,
                        original_bag=bag,
                        stripe_pid=pid,
                )
                for item_id, item_data in json.loads(bag).items():
                    product = Product.objects.get(id=item_id)
                    if isinstance(item_data, int):
                        order_line_item = OrderItem(
                            order_item=order,
                            product=product,
                            quantity=item_data,
                        )
                        order_line_item.save()
            except Exception as e:
                print('Order doesnt except >> ', order)
                if order:
                    order.delete()
                return HttpResponse(content=f'The payment has failed webhook received: {event["type"]} | Error: {e}',
                                    status=500)
        return HttpResponse(
            content=f'Webhook received: {event["type"]} | SUCCESS: Created order in webhook',
            status=200)

    def handle_payment_intent_payment_failed(self, event):
        """
        Handle the payment_intent.payment_failed webhook from Stripe
        """
        return HttpResponse(
                            content=f'The payment has failed webhook received : {event["type"]}', status=200)
