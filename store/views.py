from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from .models import Comment
from .services import *
from .forms import CommentForm
from shopping_cart.services import cart_total

from cloudipsp import Api, Checkout


def index(request):
    """Display all products and categories on main page"""

    categories = get_all_categories()

    category = request.GET.get("category")
    if category is None:
        items = get_all_products()
    elif category == "All":
        items = get_all_products()
    else:
        items = get_all_products_filtred_by_category(category)

    if request.COOKIES.get("device") != None:
        total = cart_total(request)
        return render_template_with_total_in_context(request, categories, total, items)
    else:
        return render_template_without_total_in_context(request, categories, items)


def product_detail(request, pk):
    """Display info about item"""
    item = get_product_by_id(pk)
    # Get total items in cart
    total_items_in_order = cart_total(request)
    # Add comment
    form = CommentForm()
    new_comment = comment_creation(request, item=item)
    
    context = {
        "item": item,
        "total_items_in_order": total_items_in_order,
        "form": form,
        "new_comment": new_comment,
    }
    return render(request, "store/product_page.html", context)


@login_required(login_url="login")
def product_comment(request, pk):
    """Get comments for each product"""
    comments = Comment.objects.get(id=pk)

    context = {"comments": comments}
    return render(request, "store/product_page.html", context)


@login_required(login_url="login")
def delete_comment(request, pk):
    """Delete comment"""
    comment = Comment.objects.get(id=pk)
    item = get_product_by_id(comment.product.id)
    if comment.comment_author == request.user.customer:
        comment.delete()
        return redirect("item_info", item.id)
    else:
        return redirect("item_info", item.id)



def one_click_buy_payment(request, pk):
    """Payment system"""
    product_item = Product.objects.get(id=pk)

    api = Api(merchant_id=1396424, secret_key="test")
    checkout = Checkout(api=api)
    data = {
        "currency": "USD",
        # For correct display should add '00'
        "amount": str(product_item.price) + "00",
    }
    url = checkout.url(data).get("checkout_url")
    return redirect(url)
