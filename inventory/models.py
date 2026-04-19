from django.db import models

class Product(models.Model):
    name = models.CharField(max_length=100)
    price = models.FloatField()
    quantity = models.IntegerField()
    minimum_stock = models.IntegerField(default=5)

    def __str__(self):
        return self.name

class Sale(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity_sold = models.IntegerField()
    date = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if self.product.quantity >= self.quantity_sold:
            self.product.quantity -= self.quantity_sold
            self.product.save()
        else:
            raise ValueError("Not enough stock available")

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.product.name} - {self.quantity_sold}"

class StockAdjustment(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity_changed = models.IntegerField()
    reason = models.CharField(max_length=200)
    date = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        self.product.quantity += self.quantity_changed

        if self.product.quantity < 0:
            raise ValueError("Stock cannot be negative")

        self.product.save()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.product.name} ({self.quantity_changed})"
