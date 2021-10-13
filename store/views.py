from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from shopping_cart.models import Order
from .models import Comment
from .services import *
from .forms import CommentForm

from cloudipsp import Api, Checkout


# Create your views here.


def index(request):
    """Display all products and categories on main page"""

    categories = get_all_categories()

    category = request.GET.get('category')
    if category is None:
        items = get_all_products()
    elif category == 'All':
        items = get_all_products()
    else:
        items = get_all_products_filtred_by_category(category)

    if request.user.is_authenticated:
        # Get total items in cart
        try:
            customer = request.user.customer
        except:
            device = request.COOKIES['device']
            customer, created = Customer.objects.get_or_create(device=device)

        total_items_in_order, created = Order.objects.get_or_create(
            customer=customer, complete=False)

    context = {'items': items, 'categories': categories,
               'total_items_in_order': total_items_in_order}
    return render(request, 'store/index.html', context)


def product_detail(request, pk):
    """Display info about item"""

    item = get_product_by_id(pk)

    if request.user.is_authenticated:
        # Get total items in cart
        try:
            customer = request.user.customer
        except:
            device = request.COOKIES['device']
            customer, created = Customer.objects.get_or_create(device=device)

        total_items_in_order, created = Order.objects.get_or_create(
            customer=customer, complete=False)

    # Add comment
    form = CommentForm()

    new_comment = []

    if request.method == 'POST':
        form = CommentForm(data=request.POST)
        if form.is_valid():
            # Create comment object but not save in to database yet
            new_comment = form.save(commit=False)
            # Assign the current product to the comment
            new_comment.product = item
            if request.user.is_authenticated:
                new_comment.comment_author = request.user
            else:
                return redirect('login')
            # Save the comment to the database
            new_comment.save()
            return redirect('item_info', item.id)

    context = {'item': item, 'total_items_in_order': total_items_in_order,
               'form': form, 'new_comment': new_comment}
    return render(request, 'store/product_page.html', context)


@login_required(login_url='login')
def product_comment(request, pk):
    """Get comments for each product"""

    comments = Comment.objects.get(id=pk)

    context = {'comments': comments}
    return render(request, 'store/product_page.html', context)


@login_required(login_url='login')
def delete_comment(request, pk):
    """Delete comment"""

    item = get_product_by_id(pk)
    comment = Comment.objects.get(id=pk)
    if comment.comment_author == request.user:
        comment.delete()
        return redirect('item_info', item.id)

    context = {}
    return render(request, 'store/product_page.html', context)


def one_click_buy_payment(request, pk):
    """Payment system"""
    product_item = Product.objects.get(id=pk)

    api = Api(merchant_id=1396424,
              secret_key='test')
    checkout = Checkout(api=api)
    data = {
        "currency": "USD",
        # For correct display should add '00'
        "amount": str(product_item.price) + '00'
    }
    url = checkout.url(data).get('checkout_url')
    return redirect(url)
