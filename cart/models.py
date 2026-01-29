from django.db import models
from product.models import *
from user.models import *

# Create your models here.
class Cart(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username
    
    def get_total_cost(self):
        return sum(item.get_cost() for item in self.cart_items.all())
    
    def get_total_item(self):
        return sum(item.quantity for item in self.cart_items.all())

class CartItem(models.Model):
    cart = models.ForeignKey(Cart,on_delete=models.CASCADE,related_name='cart_items')
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.product.name} - {self.quantity}"
    
    def get_cost(self):
        return self.product.price*self.quantity
