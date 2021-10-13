from django.shortcuts import render, redirect

from .models import Product, Category
from accounts.models import Customer

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
    return Product.objects.get(id=pk)



