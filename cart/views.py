from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from product.models import *
from .models import *
from .serializer import *
from rest_framework.generics import GenericAPIView
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated,AllowAny
import requests
from django.conf import settings
from django.shortcuts import redirect
from django.http import JsonResponse
from rest_framework.decorators import api_view,permission_classes

# Create your views here.
class AddToCart(APIView):
    permission_classes = [IsAuthenticated]
    def post(self,request):
        product_id = request.data.get('product_id')
        quantity = int(request.data.get('quantity',1))

        if not product_id:
            return Response({'details':'Invalid request'},status=status.HTTP_400_BAD_REQUEST)
        
        product = Product.objects.get(id=product_id)

        if quantity < 1:
            return Response({'details':'product quantity must be at last one'},status=status.HTTP_400_BAD_REQUEST)

        cart,_ = Cart.objects.get_or_create(user=request.user)

        cart_item,created  = CartItem.objects.get_or_create(
            cart=cart,
            product=product
        )

        if not created:
            cart_item.quantity += quantity
        else:
            cart_item.quantity = quantity  
        cart_item.save()    

        return Response(CartSerializer(cart).data,status=status.HTTP_200_OK)

class CartDetail(GenericAPIView):
    serializer_class = CartSerializer
    # permission_classes = [IsAuthenticated]

    def get(self,request):
        cart = Cart.objects.get(user=request.user)
        serializer = self.get_serializer(cart)
        return Response(serializer.data)
    

class UpdateCartItem(GenericAPIView):
    # permission_classes = [IsAuthenticated]
    # authentication_classes = []
    def patch(self,reuqest,item_id):
        quantity = int(reuqest.data.get('quantity',1))
        cartItem = CartItem.objects.get(id=item_id,cart__user = reuqest.user)

        if quantity < 1:
            return Response({'details':'quantity at last must be 1'},status=status.HTTP_400_BAD_REQUEST)
        
        cartItem.quantity = quantity
        cartItem.save()

        return Response({'details':'cart updated successfully'})
    

class RemoveCartItem(GenericAPIView):
    permission_classes = [IsAuthenticated]
    def delete(self,request,id):
        CartItem.objects.get(id=id,cart__user=request.user).delete()  

        return Response({'details':'Item removed'},status=status.HTTP_204_NO_CONTENT)
        
class ClearCart(GenericAPIView):
    # permission_classes = [IsAuthenticated]

    def post(self,request):
        cart = Cart.objects.get(user=request.user)
        cart.cart_items.all().delete()          
        return Response({'details':'Cart is cleared'})
        

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def sslcommerz_payment(request):
    post_data = {
        "store_id": settings.SSLCOMMERZE_STORE_ID,
        "store_passwd": settings.SSLCOMMERZE_STORE_PASSWORD,
        "total_amount": "100",
        "currency": "BDT",
        "tran_id": "TXN123456",
        "success_url": "http://127.0.0.1:8000/cart/payment/success/",
        "fail_url": "http://127.0.0.1:8000/cart/payment/fail/",
        "cancel_url": "http://127.0.0.1:8000/cart/payment/cancel/",
        "cus_name": "Mehedi Hasan",
        "cus_email": "test@gmail.com",
        "cus_add1": "Dhaka",
        "cus_city": "Dhaka",
        "cus_country": "Bangladesh",
        "cus_phone": "01700000000",
        "shipping_method": "NO",
        "product_name": "Test Product",
        "product_category": "General",
        "product_profile": "general",
    }

    url = "https://sandbox.sslcommerz.com/gwprocess/v4/api.php"
    response = requests.post(url, data=post_data)
    data = response.json()

    if data.get("status") == "SUCCESS":
        # Return Gateway URL in JSON
        return JsonResponse({"url": data["GatewayPageURL"]})
    
    return JsonResponse({"error": "Payment initiation failed"}, status=400)


def payment_success(request):
    return Response("Payment Successful ✅")

def payment_fail(request):
    return Response("Payment Failed ❌")

def payment_cancel(request):
    return Response("Payment Cancelled ⚠️")