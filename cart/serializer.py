from rest_framework import serializers
from .models import *


class CartItemSerializer(serializers.ModelSerializer):
    product_name = serializers.ReadOnlyField(source='product.name')
    product_price = serializers.ReadOnlyField(source='product.price')
    total_price = serializers.SerializerMethodField()
    class Meta:
        fields = [
            'product',
            'product_name',
            'product_price',
            'quantity',
            'total_price'
        ]       

    def get_total_price(self,obj):
        return obj.get_cost()

class CartSerializer(serializers.ModelSerializer):
    cart_items = CartItemSerializer(many=True,read_only=True)
    total_cost = serializers.SerializerMethodField()
    total_items = serializers.SerializerMethodField()

    class Meta:
        model = Cart
        fields = [
            'user',
            'cart_items',
            'total_cost',
            'total_items',
        ]         

    def get_total_cost(self,obj):
        return obj.get_total_cost()    
    
    def get_total_items(self,obj):
        return obj.get_total_item()