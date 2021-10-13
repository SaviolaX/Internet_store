from django.urls import path

from . import views


urlpatterns = [
    path('cart/', views.cart, name="cart"),
    path('add/<int:pk>/', views.add_to_cart, name='add'),
    path('del/<int:pk>/', views.delete_from_cart, name='del'),
    path('plus/<int:pk>/', views.plus_cart_item_quantity, name='plus'),
    path('minus/<int:pk>/', views.minus_cart_item_quantity, name='minus'),
    path('checkout/', views.checkout, name='checkout'),
    path('payment/', views.payment, name='payment'),

    path('', views.cart_total, name='total'),
]
