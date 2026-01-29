from rest_framework import serializers
from .models import *

class OrderItemSerializer(serializers.ModelSerializer):
    product_name = serializers.ReadOnlyField(source='product.name')  # optional: show product name
    total_cost = serializers.SerializerMethodField()

    class Meta:
        model = OrderItem
        fields = ['id', 'product', 'product_name', 'quantity', 'price', 'total_cost']

    def get_total_cost(self, obj):
        return obj.get_cost()


class OrderSerializer(serializers.ModelSerializer):
    order_items = OrderItemSerializer(many=True, read_only=True)
    total_cost = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = [
            'id',
            'user',
            'first_name',
            'last_name',
            'email',
            'phone',
            'address',
            'house_number',
            'paid',
            'transection_id',
            'status',
            'order_items',
            'total_cost',
        ]

    def get_total_cost(self, obj):
        return obj.get_total_cost()
           