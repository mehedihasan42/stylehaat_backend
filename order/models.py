from django.db import models
from product.models import *
from user.models import *
from cart.models import *
from order.models import *

# Create your models here.
class Order(models.Model):
    STATUS=[
        ('pending','Pending'),
        ('processing','Processing'),
        ('shipped','Shipped'),
        ('delivered','Delivered'),
        ('canceled','Canceled'),
    ]
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    email = models.EmailField()
    phone = models.CharField(max_length=12)
    address = models.CharField(max_length=100)
    city = models.CharField(max_length=30,default='')
    post = models.CharField(max_length=30,default='')
    house_number = models.CharField(max_length=20)
    paid = models.BooleanField(default=False)
    transection_id = models.CharField(max_length=50)
    status = models.CharField(max_length=20,choices=STATUS,default='pending')

    def __str__(self):
        return self.user.username
    
    def get_total_cost(self):
        return sum(item.get_cost() for item in self.order_items.all())
   

class OrderItem(models.Model):
    order = models.ForeignKey(Order,on_delete=models.CASCADE,related_name='order_items')
    product = models.ForeignKey(Product,on_delete=models.CASCADE)    
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=7,decimal_places=2)

    def get_cost(self):
        return self.quantity*self.price

class Payment(models.Model):
    customer = models.ForeignKey(User,on_delete=models.CASCADE)
    cart = models.ForeignKey(Cart,on_delete=models.CASCADE)
    order = models.ForeignKey(Order,on_delete=models.CASCADE)
    tran_id = models.CharField(max_length=20)
    amount = models.DecimalField(max_digits=7,decimal_places=2)
    status = models.CharField(max_length=10,choices=[
        ('pendding','Penddind'),
        ('success','Success'),
        ('fail','Fail'),
        ('cancel','Calcel')
    ],default='pendding')
    created_at = models.DateTimeField(auto_now_add=True)   
