from django.shortcuts import render
from rest_framework.generics import ListCreateAPIView,RetrieveDestroyAPIView
from django.db.models import Avg,Min,Max,Sum
from .serializer import *
from .models import *
from rest_framework.permissions import IsAuthenticated,AllowAny,IsAdminUser
from rest_framework.views import APIView
from rest_framework.response import Response
from order.models import OrderItem
from rest_framework import status
from django.shortcuts import get_object_or_404
from rest_framework.generics import RetrieveUpdateDestroyAPIView
from rest_framework.permissions import BasePermission

# Create your views here.
class SellerOnlyView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        if request.user.role != 'seller':
            return Response({"error": "Access denied"}, status=403)
        return Response({"message": "Welcome Seller"})

class IsAdminRole(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'admin'   

class CategoryListCreate(ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [AllowAny]
    authentication_classes = []

class SizeList(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        sizes = Size.objects.all().values_list('value', flat=True).distinct()
        return Response(list(sizes))

class ProductListCreate(ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    # authentication_classes = []

    def get_queryset(self):
        queryset = super().get_queryset()

        category = self.request.query_params.get('category')
        gender = self.request.query_params.get('gender')
        size = self.request.query_params.get('size')
        price_min = self.request.query_params.get('min_price')
        price_max = self.request.query_params.get('max_price')
        rating = self.request.query_params.get('rating')
        slug = self.request.query_params.get('slug')

        if price_min:
            queryset = queryset.filter(price__gte=price_min)

        if price_max:
            queryset = queryset.filter(price__lte=price_max)

        if category:
            queryset = queryset.filter(category__slug__icontains=category)

        if gender:
            queryset = queryset.filter(gender=gender)

        if size:
            queryset = queryset.filter(sizes__value=size)

        if slug:
            queryset = queryset.filter(slug=slug)

        if rating:
            queryset = queryset.annotate(
                average_rating=Avg('reviews__rating')
            ).filter(average_rating__gte=int(rating))

        return queryset

    def get_permissions(self):
        if self.request.method == 'POST':
            return [IsAdminRole()]
        return [AllowAny()]


class ProductUpdate(RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class ReviewList(ListCreateAPIView):
    serializer_class = ReviewSerializer

    def get_queryset(self):
        product_id = self.request.query_params.get('product')
        if not product_id:
            return Review.objects.none()
        return Review.objects.filter(product_id=product_id).select_related('user')
    
    def get_permissions(self):
        if self.request.method == 'GET':
            return [AllowAny()]
        return [IsAuthenticated()]

    def perform_create(self, serializer):
        request = self.request
        product_id = request.data.get('product')

        if not product_id:
            return Response('This product does not exits')
        
        product = get_object_or_404(Product,id=product_id)
        
        has_purches = OrderItem.objects.filter(
            product_id=product_id,
            order__user=request.user,
            order__paid=True
            ).exists()
        
        if not has_purches:
            raise serializers.ValidationError({"detail": "You can only review products you have purchased."}) 
        
        if Review.objects.filter(user=request.user,product=product).exists():
            raise serializers.ValidationError({'details':'You already reviewed this product'})
        
        serializer.save(user=request.user,product=product)
        