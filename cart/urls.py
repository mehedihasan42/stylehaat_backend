from django.urls import path
from .views import *

urlpatterns = [
    path('', CartDetail.as_view()),
    path('add/', AddToCart.as_view()),
    path('item/<int:item_id>/', UpdateCartItem.as_view()),
    path('item/<int:item_id>/remove/', RemoveCartItem.as_view()),
    path('clear/', ClearCart.as_view()),
]
