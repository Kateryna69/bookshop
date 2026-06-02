from django.db import models
from django.conf import settings
from shop.models import Product

# Create your models here.

class Order(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Очікує обробки'),
        ('processing', 'В обробці'),
        ('shipped', 'Відправлено'),
        ('delivered', 'Доставлено'),
        ('cancelled', 'Скасовано'),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name='orders'
    )
    first_name = models.CharField(max_length=100, verbose_name="Ім'я")
    last_name = models.CharField(max_length=100, verbose_name='Прізвище')
    email = models.EmailField(verbose_name='Email')
    phone = models.CharField(max_length=20, verbose_name='Телефон')
    city = models.CharField(max_length=100, verbose_name='Місто')
    address = models.CharField(max_length=300, verbose_name='Адреса')
    postal_code = models.CharField(max_length=20, verbose_name='Поштовий індекс')
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending',
        verbose_name='Статус'
    )
    total_price = models.DecimalField(
        max_digits=10, decimal_places=2,
        default=0,
        verbose_name='Загальна сума'
    )
    comment = models.TextField(blank=True, verbose_name='Коментар')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Замовлення'
        verbose_name_plural = 'Замовлення'
        ordering = ['-created']

    def str(self):
        return f'Замовлення #{self.id}'

    def get_total_price(self):
        return sum(item.get_cost() for item in self.items.all())


class OrderItem(models.Model):
    order = models.ForeignKey(
        Order, related_name='items',
        on_delete=models.CASCADE
    )
    product = models.ForeignKey(
        Product, related_name='order_items',
        on_delete=models.CASCADE
    )
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)

    class Meta:
        verbose_name = 'Позиція замовлення'
        verbose_name_plural = 'Позиції замовлення'

    def str(self):
        return f'{self.quantity}x {self.product.name}'

    def get_cost(self):
        return self.price * self.quantity