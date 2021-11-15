from django.db import models
from django.shortcuts import reverse

from accounts.models import Customer
# Create your models here.


class Category(models.Model):
    """Products categories"""
    category_title = models.CharField(max_length=200, blank=False, null=False)
    category_image = models.ImageField(
        upload_to='category_images/', blank=False, null=False)

    class Meta:
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.category_title


class Product(models.Model):
    """Product information"""
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, null=True)
    title = models.CharField(max_length=200, null=False, blank=False)
    price = models.IntegerField(null=False, blank=False)
    image = models.ImageField(
        upload_to='product_images/', blank=False, null=False)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.title

    def get_add_to_cart_url(self):
        return reverse("add-to-cart", kwargs={
            'pk': self.id
        })

    def get_remove_from_cart_url(self):
        return reverse("remove-from-cart", kwargs={
            'pk': self.id
        })


class Comment(models.Model):
    """Comments to products"""
    product = models.ForeignKey(
        Product, related_name='comments', on_delete=models.CASCADE)
    comment_author = models.ForeignKey(
        Customer, on_delete=models.CASCADE)
    comment_text = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_on']

    def __str__(self):
        return str(self.comment_author) + ': ' + self.comment_text[:50] + '...'
