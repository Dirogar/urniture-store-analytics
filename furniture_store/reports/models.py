from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser

User = get_user_model()

DEFAULT_AREA = 0

class Warehouse(models.Model):
    name = models.CharField(
        max_length=254,
        null=False,
        verbose_name='Склад'
    )

    class Meta:
        verbose_name = 'Склад'
        verbose_name_plural = 'Склады'

    def __str__(self):
        return self.name


class Store(models.Model):
    name = models.CharField(
        max_length=254,
        null=False,
        verbose_name='Название магазина'
    )
    area = models.FloatField(
        null=False,
        verbose_name='Площадь магазина',
        default=DEFAULT_AREA)
    warehouse = models.ForeignKey(Warehouse, on_delete=models.CASCADE)
    users = models.ManyToManyField(
        User, related_name='stores',
        blank=True,
        verbose_name='Пользователи'
    )



class Product(models.Model):
    article = models.CharField(
        primary_key=True,
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

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'

    def __str__(self):
        return self.name


class WarehouseProduct(models.Model):
    product = models.ForeignKey(
        Product,
        to_field='article',
        on_delete=models.CASCADE
    )
    warehouse = models.ForeignKey(Warehouse, on_delete=models.CASCADE)
    stock = models.IntegerField(null=False, default=0, verbose_name='Остаток')


class StoreProduct(models.Model):
    store = models.ForeignKey(Store, on_delete=models.CASCADE)
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        to_field='article'
    )
    general_plan_exhibition = models.IntegerField(null=True, blank=True)
    plan_exhibition = models.IntegerField(
        null=True,
        blank=True,
        verbose_name='План выставки'
    )
    fact_exhibition = models.IntegerField(
        null=True,
        blank=True,
        verbose_name='Факт выставки'
    )

    def __str__(self):
        return f'{self.product.name} - {self.store.name}'

    class Meta:
        verbose_name = 'Мебельный салон'
        verbose_name_plural = 'Мебельные салоны'


class Comment(models.Model):
    text = models.TextField(verbose_name='Комментарий')
    created_at = models.DateTimeField(auto_now_add=True)
    finish_planned_date = models.DateTimeField()
    product = models.ForeignKey(
        Product,
        to_field='article',
        on_delete=models.CASCADE,
        verbose_name='Товар',
        null=True
    )
    store = models.ForeignKey(Store, on_delete=models.CASCADE, null=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'

    def __str__(self):
        return self.text
