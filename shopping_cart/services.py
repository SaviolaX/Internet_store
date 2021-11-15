from .models import Order
from accounts.logic import check_user_or_guest


def cart_total(request):
    """Shows quantity items in the cart"""
    customer = check_user_or_guest(request)

    total_items_in_order, created = Order.objects.get_or_create(
        customer=customer, complete=False)

    return total_items_in_order
