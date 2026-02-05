from django.shortcuts import render
from rest_framework.decorators import api_view,permission_classes,APIView
from rest_framework.generics import ListCreateAPIView
from rest_framework.permissions import IsAuthenticated,AllowAny
from cart.models import *
from .models import *
from .serializer import *
import uuid
from django.conf import settings
import requests
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import redirect
from uuid import uuid4

# Create your views here.
class OrdersList(ListCreateAPIView):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)

class OrderItemList(ListCreateAPIView):
    serializer_class = OrderItemSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return OrderItem.objects.filter(order__user=self.request.user)

class OrderCheckoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        data = request.data

        required_fields = ['email','phone','address','city','post','house_number']
        for field in required_fields:
            if field not in data:
                return Response({"error": f"{field} is required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            cart = Cart.objects.get(user=user)
        except Cart.DoesNotExist:
            return Response({"error": "Cart not found"}, status=status.HTTP_404_NOT_FOUND)

        order = Order.objects.create(
            user=user,
            email=data['email'],
            phone=data['phone'],
            address=data['address'],
            city=data['city'],
            post=data['post'],
            house_number=data['house_number'],
            paid=False,
            transection_id=0 
        )

        for item in cart.cart_items.all():
            order.order_items.create(
                product=item.product,
                quantity=item.quantity,
                price=item.product.price
            )

        tran_id = str(uuid4())
        Payment.objects.create(
            customer=user,
            cart=cart,
            tran_id=tran_id,
            amount=cart.get_total_cost(),
            status='pendding'
        )

        post_data = {
            "store_id": settings.SSLCOMMERZE_STORE_ID,
            "store_passwd": settings.SSLCOMMERZE_STORE_PASSWORD,
            "total_amount": str(cart.get_total_cost()),
            "currency": "BDT",
            "tran_id": tran_id,
            "success_url": "http://127.0.0.1:8000/order/payment/success/",
            "fail_url": "http://127.0.0.1:8000/order/payment/fail/",
            "cancel_url": "http://127.0.0.1:8000/order/payment/cancel/",
            "cus_name": f"{user.first_name} {user.last_name}",
            "cus_email": user.email,
            "cus_add1": data['address'],
            "cus_city": data['city'],
            "cus_country": "Bangladesh",
            "cus_phone": data['phone'],
            "shipping_method": "NO",
            "product_name": "Cart Products",
            "product_category": "General",
            "product_profile": "general",
        }

        url = "https://sandbox.sslcommerz.com/gwprocess/v4/api.php"
        response = requests.post(url, data=post_data)
        result = response.json()

        if result.get("status") == "SUCCESS":
            cart.cart_items.all().delete()
            return Response({"payment_url": result["GatewayPageURL"]})

        return Response({"error": "Payment initiation failed"}, status=status.HTTP_400_BAD_REQUEST)

@csrf_exempt
@api_view(["GET", "POST"])
@permission_classes([AllowAny])
def payment_success(request):
    tran_id = request.data.get("tran_id") 
    print('tran_id: ',tran_id)
    try:
        payment = Payment.objects.get(tran_id=tran_id)
        payment.status = 'success'
        payment.save()

        order = Order.objects.get(user=payment.customer, paid=False)
        order.paid = True
        order.transection_id = tran_id
        order.save()

        for item in order.order_items.all():
            product = item.product
            product.stock -= item.quantity
            
            if product.stock < 1:
                return Response({'details':'Stock is empty'})
            product.save()

        return redirect('https://stylehaat.netlify.app/order-list')
    except Payment.DoesNotExist:
        return Response({"error": "Payment not found"}, status=404)
    except Order.DoesNotExist:
        return Response({"error": "Order not found"}, status=404)

@csrf_exempt
@api_view(["GET", "POST"])
@permission_classes([AllowAny])
def payment_fail(request):
    return redirect('https://stylehaat.netlify.app/payment-failed')

@csrf_exempt
@api_view(["GET", "POST"])
@permission_classes([AllowAny])
def payment_cancel(request):
    return redirect('https://stylehaat.netlify.app/payment-cancelled')