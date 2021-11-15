from django.shortcuts import render, redirect

from .models import Order, OrderItem
from store.models import Product
from accounts.logic import check_user_or_guest
from .services import cart_total

from cloudipsp import Api, Checkout

# Create your views here.


def cart(request):
    """Customer's cart with items"""
    customer = check_user_or_guest(request)

    order, created = Order.objects.get_or_create(
        customer=customer, complete=False)

    total_items_in_order = cart_total(request)

    context = {'order': order, 'total_items_in_order': total_items_in_order}
    return render(request, 'shopping_cart/cart_page.html', context)


def add_to_cart(request, pk):
    """Add item to the cart"""
    item = Product.objects.get(id=pk)
    # Get user account information

    customer = check_user_or_guest(request)
    order, created = Order.objects.get_or_create(
        customer=customer, complete=False)
    orderItem, created = OrderItem.objects.get_or_create(
        order=order, product=item)
    orderItem.save()
    return redirect('/')


def delete_from_cart(request, pk):
    """Delete item from the cart"""
    cart_item = OrderItem.objects.get(id=pk)
    cart_item.delete()
    return redirect('cart')


def plus_cart_item_quantity(request, pk):
    """Increse quantity of items in the cart"""
    plus_cart_item = OrderItem.objects.get(id=pk)
    plus_cart_item.quantity += 1
    plus_cart_item.save()
    return redirect('cart')


def minus_cart_item_quantity(request, pk):
    """Decrese quantity of items in the cart"""
    plus_cart_item = OrderItem.objects.get(id=pk)
    plus_cart_item.quantity -= 1
    plus_cart_item.save()
    return redirect('cart')


def checkout(request):
    """Confirmation before purchase"""
    order = cart_total(request)

    context = {'order': order}
    return render(request, 'shopping_cart/checkout_page.html', context)


def payment(request):
    """Payment system"""

    order = cart_total(request)

    total_price = order.get_cart_total
    api = Api(merchant_id=1396424,
              secret_key='test')
    checkout = Checkout(api=api)
    data = {
        "currency": "USD",
        # For correct display should add '00'
        "amount": str(total_price) + '00'
    }
    url = checkout.url(data).get('checkout_url')
    return redirect(url)
