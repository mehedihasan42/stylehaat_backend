from django.db import models
from django.core.validators import MaxValueValidator,MinValueValidator
from ckeditor.fields import RichTextField
from user.models import *

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=150)
    slug = models.SlugField(max_length=150)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = 'categoris'

    def __str__(self):
        return self.name

class Size(models.Model):
    
    value = models.CharField(max_length=10, unique=True)

    def __str__(self):
        return self.value
    

class Product(models.Model):

    GENDER=[
    ('male','Male'),
    ('female','Female')
    ]

    image = models.URLField()
    title = models.CharField(max_length=150)
    slug = models.SlugField(max_length=150)
    description = models.TextField()    
    price = models.IntegerField()
    stock = models.IntegerField()
    available = models.BooleanField(default=True)
    sizes = models.ManyToManyField(Size, related_name='products')
    gender = models.CharField(max_length=15,choices=GENDER)
    category = models.ForeignKey(Category,on_delete=models.CASCADE)
    user = models.ForeignKey(User,on_delete=models.CASCADE)

    def __str__(self):
        return self.title
    
    def average_rating(self):
        reviews = self.reviews.all()
        if reviews.count() > 0:
          return sum(rating.rating for rating in reviews)
        
        
class Review(models.Model):
    rating = models.SmallIntegerField(validators=[MaxValueValidator(5),MinValueValidator(1)])
    comment = models.TextField()
    product = models.ForeignKey(Product,on_delete=models.CASCADE,related_name='reviews')
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.rating}"
