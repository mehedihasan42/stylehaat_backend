from django.shortcuts import render
from rest_framework.generics import ListCreateAPIView,RetrieveDestroyAPIView
from django.db.models import Avg,Min,Max,Sum
from .serializer import *
from .models import *
from rest_framework.permissions import IsAuthenticated,AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response
from order.models import OrderItem
from rest_framework import status

# Create your views here.
class SellerOnlyView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        if request.user.role != 'seller':
            return Response({"error": "Access denied"}, status=403)
        return Response({"message": "Welcome Seller"})

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
    permission_classes = [AllowAny]
    authentication_classes = []

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

class ReviewList(ListCreateAPIView):
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        product = self.request.query_params.get('product')
        return Review.objects.filter(product=product)

    def post(self,request,*args, **kwargs):
        product_id = request.data.get('product')
        product = Product.objects.get(id=product_id)
        rating = request.data.get('rating')
        comment = request.data.get('comment', '')
        purchased_items = OrderItem.objects.filter(
                                            order__user=request.user,
                                            product_id=product_id,
                                            order__paid=True
                                            )
        if not purchased_items.exists():
            return Response({'details':'You can only review products you have purchased.'})
        serializer = self.get_serializer(data={
            'product': product_id,
            'rating': rating,
            'comment': comment
        })

        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data,status=status.HTTP_201_CREATED)    
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)