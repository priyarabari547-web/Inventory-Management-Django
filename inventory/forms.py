from django import forms
from .models import Product,Sale,StockAdjustment

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'price', 'quantity', 'minimum_stock']

class SaleForm(forms.ModelForm):
    class Meta:
        model = Sale
        fields = ['product', 'quantity_sold']

class StockAdjustmentForm(forms.ModelForm):
    class Meta:
        model = StockAdjustment
        fields = ['product', 'quantity_changed', 'reason']