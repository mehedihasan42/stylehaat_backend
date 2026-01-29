from django.db import models
from product.models import *
from user.models import *

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
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField()
    phone = models.CharField(max_length=12)
    address = models.CharField(max_length=100)
    house_number = models.CharField(max_length=20)
    paid = models.BooleanField(default=False)
    transection_id = models.SmallIntegerField()
    status = models.CharField(max_length=20,choices=STATUS)

    def __str__(self):
        return self.user.username
    
    def get_total_cost(self):
        return sum(item.get_cost() for item in self.order_items.all())

class OrderItem(models.Model):
    order = models.ForeignKey(Order,on_delete=models.CASCADE,related_name='order_items')
    product = models.ForeignKey(Product,on_delete=models.CASCADE)    
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=4,decimal_places=2)

    def get_cost(self):
        return self.quantity*self.product.price
    