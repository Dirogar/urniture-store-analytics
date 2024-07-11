from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser

User = get_user_model()

DEFAULT_AREA = 0

class Shop(models.Model):
    name = models.CharField(
        max_length=254,
        null=False,
        verbose_name='Название магазина'
    )
    area = models.FloatField(
        null=False,
        verbose_name='Площадь магазина',
        default=DEFAULT_AREA)
    plan = models.IntegerField(
        null=True,
        verbose_name='Планируется выставить товара'
    )
    fact = models.IntegerField(
        null=True,
        verbose_name='Факт выставленного товара'
    )
    deviation = models.IntegerField(null=True, verbose_name='Отклонение')
    members = models.ManyToManyField(User, related_name='Магазины')

class Product(models.Model):
    article = models.CharField(
        max_length=9,
        null=False,
        verbose_name='Артикул'
    )
    name = models.CharField(
        max_length=254,
        null=False,
        verbose_name='Номенклатура'
    )
    model = models.CharField(
        max_length=254,
        null=True,
        verbose_name='Модель'
    )
    manufacturer = models.CharField(
        max_length=254,
        null=True,
        verbose_name='Производитель'
    )
    square = models.FloatField(
        null=True,
        verbose_name='Площадь номенклатуры'
    )
    category = models.CharField(
        max_length=254,
        null=True,
        verbose_name='Категория'
    )
    segment = models.CharField(
        max_length=254,
        null=True,
        verbose_name='Сегмент'
    )
    matrix = models.CharField(
        max_length=254,
        null=True,
        verbose_name='Матрица'
    )
    shops = models.ManyToManyField(Shop, related_name='shops')

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'

    def __str__(self):
        return self.name


class Warehouse(models.Model):
    name = models.CharField(
        max_length=254,
        null=False,
        verbose_name='Склад'
    )
    warehouse_remains = models.IntegerField(
        null=True,
        verbose_name='Остатки склада'
    )
    product = models.ManyToManyField(
        Product,
        related_name='Товар'
    )

    class Meta:
        verbose_name = 'Склад'
        verbose_name_plural = 'Склады'

    def __str__(self):
        return self.name


    class Meta:
        verbose_name = 'Мебельный салон'
        verbose_name_plural = 'Мебельные салоны'

    def __str__(self):
        return self.name


class Comment(models.Model):
    text = models.TextField(verbose_name='Комментарий')
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        verbose_name='Товар',
        null=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'

    def __str__(self):
        return self.name
