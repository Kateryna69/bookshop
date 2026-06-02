# from django.db import models
# from django.urls import reverse
# from django.utils.text import slugify
# import uuid

# # Create your models here.

# class Category(models.Model):
#     name = models.CharField(max_length=200, verbose_name='Назва')
#     slug = models.SlugField(max_length=200, unique=True)
#     icon = models.CharField(max_length=50, default='📚', verbose_name='Іконка')
#     parent = models.ForeignKey(
#         'self', null=True, blank=True,
#         related_name='children',
#         on_delete=models.CASCADE,
#         verbose_name='Батьківська категорія'
#     )

#     class Meta:
#         verbose_name = 'Категорія'
#         verbose_name_plural = 'Категорії'
#         ordering = ['name']

#     def str(self):
#         return self.name

#     def get_absolute_url(self):
#         return reverse('shop:product_list_by_category', args=[self.slug])


# class Product(models.Model):
#     category = models.ForeignKey(
#         Category, related_name='products',
#         on_delete=models.CASCADE,
#         verbose_name='Категорія'
#     )
#     name = models.CharField(max_length=200, verbose_name='Назва')
#     slug = models.SlugField(max_length=200, unique=True)
#     author = models.CharField(max_length=200, verbose_name='Автор')
#     publisher = models.CharField(max_length=200, blank=True, verbose_name='Видавництво')
#     description = models.TextField(blank=True, verbose_name='Опис')
#     cover = models.ImageField(upload_to='books/%Y/%m/', blank=True, verbose_name='Обкладинка')
#     price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Ціна')
#     old_price = models.DecimalField(
#         max_digits=10, decimal_places=2,
#         null=True, blank=True,
#         verbose_name='Стара ціна'
#     )
#     stock = models.PositiveIntegerField(default=0, verbose_name='Залишок')
#     available = models.BooleanField(default=True, verbose_name='Доступний')
#     is_featured = models.BooleanField(default=False, verbose_name='Хіт продажів')
#     rating = models.DecimalField(
#         max_digits=3, decimal_places=1,
#         default=5.0, verbose_name='Рейтинг'
#     )
#     rating_count = models.PositiveIntegerField(default=0, verbose_name='Кількість оцінок')
#     created = models.DateTimeField(auto_now_add=True)
#     updated = models.DateTimeField(auto_now=True)

#     class Meta:
#         verbose_name = 'Книга'
#         verbose_name_plural = 'Книги'
#         ordering = ['-created']

#     def str(self):
#         return self.name

#     def save(self, *args, **kwargs):
#         if not self.slug:
#             base_slug = slugify(self.name, allow_unicode=True)
#             slug = base_slug
#             counter = 1
#             while Product.objects.filter(slug=slug).exists():
#                 slug = f"{base_slug}-{counter}"
#                 counter += 1
#             self.slug = slug
#         super().save(*args, **kwargs)

#     def get_absolute_url(self):
#         return reverse('shop:product_detail', args=[self.slug])

#     @property
#     def discount_percent(self):
#         if self.old_price and self.old_price > self.price:
#             return int((1 - self.price / self.old_price) * 100)
#         return 0
from django.db import models
from django.urls import reverse
from django.utils.text import slugify


class Category(models.Model):
    name = models.CharField(max_length=200, verbose_name='Назва')
    slug = models.SlugField(max_length=200, unique=True)
    icon = models.CharField(max_length=50, default='📚', verbose_name='Іконка')
    parent = models.ForeignKey(
        'self', null=True, blank=True,
        related_name='children',
        on_delete=models.CASCADE,
        verbose_name='Батьківська категорія'
    )

    class Meta:
        verbose_name = 'Категорія'
        verbose_name_plural = 'Категорії'
        ordering = ['name']

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('shop:product_list_by_category', args=[self.slug])


class Product(models.Model):
    category = models.ForeignKey(
        Category, related_name='products',
        on_delete=models.CASCADE,
        verbose_name='Категорія'
    )
    name = models.CharField(max_length=200, verbose_name='Назва')
    slug = models.SlugField(max_length=200, unique=True)
    author = models.CharField(max_length=200, verbose_name='Автор')
    publisher = models.CharField(max_length=200, blank=True, verbose_name='Видавництво')
    description = models.TextField(blank=True, verbose_name='Опис')
    cover = models.ImageField(upload_to='books/%Y/%m/', blank=True, verbose_name='Обкладинка')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Ціна')
    old_price = models.DecimalField(
        max_digits=10, decimal_places=2,
        null=True, blank=True, verbose_name='Стара ціна'
    )
    stock = models.PositiveIntegerField(default=0, verbose_name='Залишок')
    available = models.BooleanField(default=True, verbose_name='Доступний')
    is_featured = models.BooleanField(default=False, verbose_name='Хіт продажів')
    rating = models.DecimalField(
        max_digits=3, decimal_places=1,
        default=5.0, verbose_name='Рейтинг'
    )
    rating_count = models.PositiveIntegerField(default=0, verbose_name='Кількість оцінок')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Книга'
        verbose_name_plural = 'Книги'
        ordering = ['-created']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            translit_map = {
                'а': 'a', 'б': 'b', 'в': 'v', 'г': 'g', 'д': 'd',
                'е': 'e', 'є': 'ye', 'ж': 'zh', 'з': 'z', 'и': 'i',
                'і': 'i', 'ї': 'yi', 'й': 'y', 'к': 'k', 'л': 'l',
                'м': 'm', 'н': 'n', 'о': 'o', 'п': 'p', 'р': 'r',
                'с': 's', 'т': 't', 'у': 'u', 'ф': 'f', 'х': 'kh',
                'ц': 'ts', 'ч': 'ch', 'ш': 'sh', 'щ': 'shch',
                'ь': '', 'ю': 'yu', 'я': 'ya', 'ё': 'yo', 'ъ': '',
            }
            name_lower = self.name.lower()
            transliterated = ''
            for char in name_lower:
                transliterated += translit_map.get(char, char)
            base_slug = slugify(transliterated)
            if not base_slug:
                base_slug = f'book-{id(self)}'
            slug = base_slug
            counter = 1
            while Product.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f'{base_slug}-{counter}'
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('shop:product_detail', args=[self.slug])

    @property
    def discount_percent(self):
        if self.old_price and self.old_price > self.price:
            return int((1 - self.price / self.old_price) * 100)
        return 0
class Wishlist(models.Model):
    user = models.ForeignKey(
        'accounts.CustomUser',
        on_delete=models.CASCADE,
        related_name='wishlist'
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='wishlisted_by'
    )
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'product')
        verbose_name = 'Бажане'
        verbose_name_plural = 'Бажане'

    def __str__(self):
        return f'{self.user.email} — {self.product.name}'