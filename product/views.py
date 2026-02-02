from django.shortcuts import render
from rest_framework.generics import ListCreateAPIView,RetrieveDestroyAPIView
from django.db.models import Avg,Min,Max,Sum
from .serializer import *
from .models import *
from rest_framework.permissions import IsAuthenticated,AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response

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


