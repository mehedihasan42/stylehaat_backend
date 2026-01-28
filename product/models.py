from django.db import models
from django.core.validators import MaxValueValidator,MinValueValidator

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

GENDER=[
    ('male','Male'),
    ('female','Female')
]
class Product(models.Model):
    image = models.URLField()
    title = models.CharField(max_length=150)
    description = models.TextField()    
    price = models.DecimalField(max_digits=4,decimal_places=2)
    stock = models.IntegerField()
    available = models.BooleanField(default=False)
    size = models.CharField(max_length=10)
    gender = models.CharField(max_length=15)
    category = models.ForeignKey(Category,on_delete=models.CASCADE)

class Review(models.Model):
    rating = models.SmallIntegerField(validators=[MaxValueValidator(5),MinValueValidator(1)])
    comment = models.TextField()
    user = models.ForeignKey()