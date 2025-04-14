from django.db import models
from django.urls import reverse

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
    description = models.TextField(blank=True)
    slug = models.SlugField(max_length=250)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    image = models.ImageField(upload_to='images/')
    stock = models.PositiveIntegerField(default=0)  # Controle de estoque
    made_in_mari = models.BooleanField(default=False)  # Fabricado em Mari
    
    class Meta:
        verbose_name_plural = "products"
        indexes = [
            models.Index(fields=['title']),
            models.Index(fields=['price']),
            models.Index(fields=['stock']),
            models.Index(fields=['made_in_mari']),
        ]
    
    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('product-info', args=[self.slug])
    
    def is_in_stock(self):
        return self.stock > 0