from django import forms
from .models import Product, Category, Supplier, StockMovement


class CategoryCreateForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = [
            'name',
            'description'
        ]

        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }



class SupplierCreateForm(forms.ModelForm):
    class Meta:
        model = Supplier
        fields = [
            'name',
            'contact',
            'phone',
            'email'
        ]

        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'contact': forms.TextInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
        }


class ProductCreateForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = [
            'sku',
            'name',
            'description',
            'price',
            'stock',
            'min_stock',
            'category',
            'supplier'
        ]

        widgets = {
            'sku': forms.TextInput(attrs={'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'price': forms.NumberInput(attrs={'class': 'form-control'}),
            'stock': forms.NumberInput(attrs={'class': 'form-control'}),
            'min_stock': forms.NumberInput(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'supplier': forms.Select(attrs={'class': 'form-control'}),
        }


class StockMovementCreateForm(forms.ModelForm):
    class Meta:
        model = StockMovement
        fields = [
            'product',
            'movement_type',
            'quantity',
            'notes'
        ]

        widgets = {
            'product': forms.Select(attrs={'class': 'form-control'}),
            'movement_type': forms.Select(attrs={'class': 'form-control'}),
            'quantity': forms.NumberInput(attrs={'class': 'form-control'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }


class CSVImportForm(forms.Form):
    csv_file = forms.FileField(label="Selecciona tu archivo CSV", widget=forms.FileInput(attrs={'class': 'form-control'}))