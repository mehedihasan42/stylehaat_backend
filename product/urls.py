from django.urls import path
from rest_framework import routers
from .views import *

urlpatterns = [
    path('category/', CategoryListCreate.as_view(), name='category-list-create'),
    path('products/', ProductListCreate.as_view(), name='product-list-create'),
    path('product/<int:pk>/', ProductUpdate.as_view(), name='product-details'),
    path('reviews/', ReviewList.as_view(), name='product-list-create'),
    path('sizes/', SizeList.as_view(), name='size-list'),
]
