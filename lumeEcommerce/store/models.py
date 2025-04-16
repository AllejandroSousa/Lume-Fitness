from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User

# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=250, db_index=True)
    slug = models.SlugField(max_length=250, unique=True)  #Only unique categories

    class Meta:
        verbose_name_plural = "categories"  #Renaming the Category page in Django's admin panel

    def __str__(self):
        return self.name  #Renaming categories on the Category page in Django's admin panel

    def get_absolute_url(self):
        return reverse('list-category', args=[self.slug])

class Product(models.Model):
    category = models.ForeignKey(Category, related_name='product', on_delete=models.CASCADE, null=True)
    title = models.CharField(max_length=250)
    brand = models.CharField(max_length=250, default='Sem marca')
    description = models.TextField(blank=True)  #Optional
    slug = models.SlugField(max_length=250)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    image = models.ImageField(upload_to='images/')
    stock = models.PositiveIntegerField(default=0)  # New field to track stock quantity
    is_made_in_mari = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = "products"  #Renaming the Product page in Django's admin panel

    def __str__(self):
        return self.title  #Renaming products on the Product page in Django's admin panel

    def get_absolute_url(self):
        return reverse('product-info', args=[self.slug])
    

class Seller(models.Model):
    name = models.CharField(max_length=100)
    user = models.OneToOneField(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='seller_profile'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name