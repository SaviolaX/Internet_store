from django.shortcuts import render, redirect, get_object_or_404

from .models import Product, Category
from .forms import CommentForm

# from django.http import request


def get_all_categories():
    """Get all categories from db"""
    return Category.objects.all()


def get_all_products():
    """Get all products from db"""
    return Product.objects.all()


def get_all_products_filtred_by_category(category):
    """Filtered products by category"""
    return Product.objects.filter(category__category_title=category)


def get_product_by_id(pk):
    """Get item by id"""
    return get_object_or_404(Product, id=pk)


def comment_creation(request, item):
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
                new_comment.comment_author = request.user.customer
            else:
                return redirect('login')
            # Save the comment to the database
            new_comment.save()
            return redirect('item_info', item.id)


def render_template_with_total_in_context(request, categories, total, items):
    context = {'items': items, 'categories': categories, 'total': total}
    return render(request, 'store/index.html', context)


def render_template_without_total_in_context(request, categories, items):
    context = {'items': items, 'categories': categories}
    return render(request, 'store/index.html', context)
