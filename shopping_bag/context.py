from decimal import Decimal
from django.conf import settings
from django.shortcuts import get_object_or_404
from products.models import Product

#This context processor was taken directly from the CI walkalong project Boutique Ado

def bag_contents(request):

    bag_items = []
    total = 0
    product_count = 0
    bag = request.session.get('bag', {})
    print(" step 1 bag_items > ", bag_items)
    print(" step 1 total > ", total)
    print(" step 1 product_count > ", product_count)
    print(" step 1 bag > ", bag)

    for item_id, item_data in bag.items():
        if isinstance(item_data, int):
            product = get_object_or_404(Product, pk=item_id)
            total += item_data * product.price
            product_count += item_data
            bag_items.append({
                'item_id': item_id,
                'quantity': item_data,
                'product': product,
            })
            print("step 2 look here price > ", product.price)
            print("step 2 look here item_data > ", item_data)
            print("step 2 look here total > ", total)
            print("step 2 look here bag_items > ", bag_items)
        else:
            product = get_object_or_404(Product, pk=item_id)
            for size, quantity in item_data['items_by_size'].items():
                total += quantity * product.price
                product_count += quantity
                bag_items.append({
                    'item_id': item_id,
                    'quantity': quantity,
                    'product': product,
                    'size': size,
                })
                print("step else look here price > ", product)
                print("step else look here item_data > ", size)
                print("step else look here total > ", quantity)
                print("step else look here bag_items > ", product_count)

    if total < settings.FREE_DELIVERY_THRESHOLD:
        delivery = 10
        print("look at me delivery > :", delivery)
        free_delivery_delta = settings.FREE_DELIVERY_THRESHOLD - total
        print("look at me delivery delta line 52> :", free_delivery_delta)
    else:
        delivery = 0
        free_delivery_delta = 0

    grand_total = delivery + total

    context = {
        'bag_items': bag_items,
        'total': total,
        'product_count': product_count,
        'delivery': delivery,
        'free_delivery_delta': free_delivery_delta,
        'free_delivery_threshold': settings.FREE_DELIVERY_THRESHOLD,
        'grand_total': grand_total,
    }
    print("This is the context >> ", context)

    print("step 3 look here settings.FREE_DELIVERY_THRESHOLD > ", settings.FREE_DELIVERY_THRESHOLD)
    print("step 3 look here delivery> ", delivery)
    print("step 3 look here total> ", total)
    print("step 3 look here grand_total> ", grand_total)
    print("step 3 look here free_delivery_delta> ", free_delivery_delta)

    return context
