from django.contrib import admin
from .models import Product, Sale, StockAdjustment

admin.site.register(Product)
admin.site.register(Sale)
admin.site.register(StockAdjustment)