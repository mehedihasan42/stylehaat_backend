from django.urls import path
from .views import *

urlpatterns = [
    path("checkout/", OrderCheckoutView.as_view(), name="order-checkout"),
    path("list/",OrdersList.as_view()),
    path("item_list/",OrderItemList.as_view()),
    path("payment/success/", payment_success),
    path("payment/fail/", payment_fail),
    path("payment/cancel/", payment_cancel),
]
