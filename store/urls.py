from django.urls import path

from . import views


urlpatterns = [
    # Display products
    path('', views.index, name='index'),
    path('item/<int:pk>/', views.product_detail, name='item_info'),
    path('comments/<int:pk>/', views.product_comment, name='comments'),
    path('del_comment/<str:pk>/', views.delete_comment, name='del_comment'),
    path('1click_buy/<int:pk>/', views.one_click_buy_payment, name='buy'),
]
