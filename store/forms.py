from django import forms
from .models import Product,Category

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'category', 'image', 'weight', 'mrp', 'selling_price', 'is_hot_deal']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex: Onion (Savala)'}),
            'weight': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex: 1 kg'}),
            'mrp': forms.NumberInput(attrs={'class': 'form-control'}),
            'selling_price': forms.NumberInput(attrs={'class': 'form-control'}),
            'image': forms.FileInput(attrs={'class': 'form-control'}),
        }

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'image']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Category Name'}),
            'image': forms.FileInput(attrs={'class': 'form-control'}),
        }