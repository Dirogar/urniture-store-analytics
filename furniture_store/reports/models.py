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
    users = models.ManyToManyField(
        User,
        related_name='stores',
        blank=True,
        verbose_name='Пользователи'
    )

    class Meta:
        verbose_name = 'Магазин'
        verbose_name_plural = 'Магазины'

    def __str__(self):
        return self.name

class RoomClass(models.Model):
    name = models.CharField(max_length=5, unique=True)

    class Meta:
        verbose_name = 'Класс комнаты'
        verbose_name_plural = 'Классы комнат'

    def __str__(self):
        return self.name


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
    room_class = models.ForeignKey(
        RoomClass,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='products'
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
        on_delete=models.CASCADE,
        related_name='warehouse_products'
    )
    warehouse = models.ForeignKey(
        Warehouse,
        on_delete=models.CASCADE,
        related_name='warehouse_products'
    )
    stock = models.IntegerField(null=False, default=0, verbose_name='Остаток')

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['warehouse', 'product'], name='unique_warehouse_product')
        ]
        verbose_name = 'Продукт на складе'
        verbose_name_plural = 'Продукты на складе'


class StoreProduct(models.Model):
    store = models.ForeignKey(
        Store,
        on_delete=models.CASCADE,
        related_name='store_products'
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        to_field='article',
        related_name='store_products'
    )
    plan_exhibition = models.IntegerField(
        null=False,
        blank=False,
        default=0,
        verbose_name='План выставки'
    )
    fact_exhibition = models.IntegerField(
        null=False,
        blank=False,
        default=0,
        verbose_name='Факт выставки'
    )
    deviation = models.IntegerField(
        null=False,
        blank=False,
        default=0,
        verbose_name='Отклонение'

    )

    def __str__(self):
        return f'{self.product.name} - {self.store.name}'

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['store', 'product'],
                                    name='unique_store_product')
            ]
        verbose_name = 'Мебельный салон'
        verbose_name_plural = 'Мебельные салоны'


class Comment(models.Model):
    text = models.TextField(verbose_name='Комментарий')
    created_at = models.DateTimeField(auto_now_add=True)
    finish_planned_date = models.DateTimeField(
        verbose_name='Планируемая дата выполнения'
    )
    product = models.ForeignKey(
        Product,
        to_field='article',
        on_delete=models.CASCADE,
        verbose_name='Товар',
        null=True,
        db_column='product_article',
        related_name='comments'
    )
    store = models.ForeignKey(
        Store,
        on_delete=models.CASCADE,
        null=True,
        related_name='comments'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments'
    )

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'

    def __str__(self):
        return self.text

