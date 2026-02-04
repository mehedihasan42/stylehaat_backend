from rest_framework import serializers
from .models import *

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'slug']


class ReviewSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)  
    username = serializers.CharField(source='user.username', read_only=True)

    class Meta:
        model = Review
        fields = '__all__'


class SizeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Size
        fields = ['value']


class ProductSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    user = serializers.StringRelatedField(read_only=True) 
    reviews = ReviewSerializer(many=True, read_only=True)
    average_rating = serializers.SerializerMethodField()
    sizes = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = [
            'id', 'image', 'title', 'slug', 'description', 'price', 'stock',
            'available', 'sizes', 'gender', 'category', 'user', 'reviews', 'average_rating'
        ]

    def get_average_rating(self, obj):
        reviews = obj.reviews.all()
        if reviews.exists():
            return round(sum(r.rating for r in reviews) / reviews.count())
        return None     
    
    def get_sizes(self,obj):
        return [size.value for size in obj.sizes.all()]
     