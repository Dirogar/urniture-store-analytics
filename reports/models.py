from django.db import models
from django.contrib import admin
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser
from .validators import validate_future_date

User = get_user_model()

DEFAULT_AREA = 0

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    work_position = models.TextField(
        max_length=100,
        blank=True,
        verbose_name='Должность'
    )

    class Meta:
        verbose_name = 'Допольнительная информация'


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()


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
    info = models.TextField(
        null=True,
        blank=True,
        verbose_name='Информация о салоне'
    )

    class Meta:
        verbose_name = 'Магазин'
        verbose_name_plural = 'Магазины'

    def __str__(self):
        return self.name


class ProductCategory(models.Model):
    id = models.CharField(
        primary_key=True,
        max_length=18,
        null=False,
        verbose_name='Код'
    )
    name = models.CharField(max_length=128, unique=True)

    class Meta:
        verbose_name = 'Категория',
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name


class Product(models.Model):
    article = models.CharField(
        primary_key=True,
        max_length=16,
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
    category = models.ForeignKey(
        ProductCategory,
        to_field='id',
        on_delete=models.DO_NOTHING,
        verbose_name='Категория',
        related_name='category_product',
        null=True,
        blank=True
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
    room_class = models.CharField(
        max_length=8,
        null=True,
        blank=True,
        verbose_name='Класс комнаты'
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
        on_delete=models.DO_NOTHING,
        related_name='warehouse_products',
        db_column='product_article',
    )
    warehouse = models.ForeignKey(
        Warehouse,
        on_delete=models.DO_NOTHING,
        related_name='warehouse_products'
    )
    stock = models.IntegerField(null=True, default=0, verbose_name='Остаток')

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['warehouse', 'product'],
                                    name='unique_warehouse_product')
        ]
        verbose_name = 'Продукт на складе'
        verbose_name_plural = 'Продукты на складе'


class StoreProduct(models.Model):
    store = models.ForeignKey(
        Store,
        on_delete=models.DO_NOTHING,
        related_name='store_products'
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.DO_NOTHING,
        to_field='article',
        related_name='store_products',
        db_column='product_article',
    )
    plan_exhibition = models.IntegerField(
        null=True,
        blank=True,
        verbose_name='План выставки'
    )
    fact_exhibition = models.IntegerField(
        null=True,
        blank=True,
        default=0,
        verbose_name='Факт выставки'
    )
    deviation = models.IntegerField(
        null=True,
        blank=True,
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
        verbose_name='Планируемая дата выполнения',
        validators=[validate_future_date]
    )
    product = models.ForeignKey(
        Product,
        to_field='article',
        on_delete=models.DO_NOTHING,
        verbose_name='Товар',
        null=True,
        db_column='product_article',
        related_name='comments'
    )
    store = models.ForeignKey(
        Store,
        on_delete=models.DO_NOTHING,
        null=True,
        related_name='comments'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.DO_NOTHING,
        related_name='comments'
    )
    status = models.CharField(
        max_length=56,
        null=False,
        default='Не выполнено',
        verbose_name= 'Статус комментария'
    )

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'

    def __str__(self):
        return self.text
