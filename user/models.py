from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
    ROLE=[
        ('admin','Admin'),
        ('seller','Seller'),
        ('customer','Customer')
    ]
    email = models.EmailField()
    phone = models.CharField(max_length=12)
    role = models.CharField(max_length=15,choices=ROLE)
    
    def __str__(self):
        return f"{self.username} - {self.role}"
