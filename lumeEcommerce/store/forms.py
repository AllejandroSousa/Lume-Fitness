from django import forms
from .models import Product, Category

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['category', 'title', 'brand', 'description', 'slug', 'price', 'image']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4, 'cols': 40}),
            'category': forms.Select(),
        }

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'slug']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'slug': forms.TextInput(attrs={'class': 'form-control'}),
        }