from django.urls import path
from .views import *

urlpatterns = [
    path('', CartDetail.as_view()),
    path('add/', AddToCart.as_view()),
    path('update/<int:item_id>/', UpdateCartItem.as_view()),
    path('remove/<int:id>/', RemoveCartItem.as_view()),
    path('clear/', ClearCart.as_view()),
    path("pay/", sslcommerz_payment),
    path("payment/success/", payment_success),
    path("payment/fail/", payment_fail),
    path("payment/cancel/", payment_cancel),
]
