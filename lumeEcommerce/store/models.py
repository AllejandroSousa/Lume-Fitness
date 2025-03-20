from django.db import models


# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=250, db_index=True)
    slug = models.SlugField(max_length=250, unique=True)  #Only unique categories

    class Meta:
        verbose_name_plural = "categories"  #Renaming the Category page in Django's admin panel

    def __str__(self):
        return self.name  #Renaming categories on the Category page in Django's admin panel


class Product(models.Model):
    category = models.ForeignKey(Category, related_name='product', on_delete=models.CASCADE, null=True)
    title = models.CharField(max_length=250)
    brand = models.CharField(max_length=250, default='Sem marca')
    description = models.TextField(blank=True)  #Optional
    slug = models.SlugField(max_length=250)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    image = models.ImageField(upload_to='images/')

    class Meta:
        verbose_name_plural = "products"  #Renaming the Product page in Django's admin panel

    def __str__(self):
        return self.title  #Renaming products on the Product page in Django's admin panel
