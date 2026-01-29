from django.shortcuts import render
from rest_framework.generics import ListCreateAPIView
from django.db.models import Avg,Min,Max,Sum
from .serializer import *
from .models import *

# Create your views here.
class CategoryListCreate(ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class ProductListCreate(ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def get_queryset(self):
        request = self.request
        queryset = super().get_queryset()
        category = request.query_params.get('category')
        gender = request.query_params.get('gender')
        size = request.query_params.get('size')
        price_max = request.query_params.get('min_price')
        price_min = request.query_params.get('max_price')

        if price_max:
            queryset = queryset.filter(price__gte=price_max)

        if price_min:
            queryset = queryset.filter(price__lte=price_min)    

        if category:
            queryset = queryset.filter(category_id=category)

        if gender:
            queryset = queryset.filter(gender=gender)    

        if size:
            queryset = queryset.filter(size=size)    

        return queryset