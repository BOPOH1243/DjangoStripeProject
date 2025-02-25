from django.db import models
from decimal import Decimal

class Item(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(
        max_length=3,
        default='usd',
        choices=[('usd', 'USD'), ('eur', 'EUR')]
    )

    def __str__(self):
        return self.name

class Discount(models.Model):
    name = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=10, decimal_places=2)  # Сумма скидки или процент
    is_percentage = models.BooleanField(default=False)

    def __str__(self):
        return self.name

class Tax(models.Model):
    name = models.CharField(max_length=255)
    percentage = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return self.name

class Order(models.Model):
    session_key = models.CharField(max_length=40, unique=True)
    items = models.ManyToManyField(Item, blank=True)
    discounts = models.ManyToManyField(Discount, blank=True)
    taxes = models.ManyToManyField(Tax, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def total_amount(self):
        total = sum(item.price for item in self.items.all())
        # Применяем скидки
        for discount in self.discounts.all():
            if discount.is_percentage:
                total -= total * (discount.amount / Decimal('100'))
            else:
                total -= discount.amount
        # Применяем налоги
        for tax in self.taxes.all():
            total += total * (tax.percentage / Decimal('100'))
        return total

    def order_currency(self):
        # Предполагаем, что все товары в заказе имеют одну валюту
        if self.items.exists():
            return self.items.first().currency
        return 'usd'

    def __str__(self):
        return f"Order {self.id} (Session: {self.session_key})"
