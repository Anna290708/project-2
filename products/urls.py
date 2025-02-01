from django.urls import path
from products.views import *

urlpatterns=[
    path('products/', products_view, name='products'),
    path('reviews/', review_view, name="reviews"),
    path('cart/', cart_view, name='cart'),
    path('tags/<int:product_id>/', product_tag_view, name='product_tags'),
    path('favourites/<int:user_id>/', favorite_product_view, name='favorite_product_view'),
    ]