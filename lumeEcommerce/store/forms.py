from django import forms
from .models import Product, Category

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['category', 'title', 'brand', 'description', 'slug', 'price', 'image', 'stock', 'is_made_in_mari']
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

class ProductFilterForm(forms.Form):
    name = forms.CharField(required=False, label='Product Name', widget=forms.TextInput(attrs={'class': 'form-control'}))
    min_price = forms.DecimalField(required=False, label='Min Price', widget=forms.NumberInput(attrs={'class': 'form-control'}))
    max_price = forms.DecimalField(required=False, label='Max Price', widget=forms.NumberInput(attrs={'class': 'form-control'}))
    category = forms.ModelChoiceField(queryset=Category.objects.all(), required=False, label='Category', widget=forms.Select(attrs={'class': 'form-control'}))
    is_made_in_mari = forms.BooleanField(required=False, label='Made in Mari', widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}))
