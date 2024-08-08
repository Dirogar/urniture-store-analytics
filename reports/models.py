"""Модели приложения reports."""
from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission
from .validators import validate_future_date

DEFAULT_AREA = 0


class WorkPosition(models.Model):
    """Должность сотрудника."""

    name = models.CharField(
        max_length=100,
        null=True,
        blank=True,
        verbose_name='Нзавние должности'
    )

    class Meta:
        """Русское название модели."""

        verbose_name = 'Должность'
        verbose_name_plural = 'Должности'

    def __str__(self):
        """Возвращает название поля."""
        return self.name


class City(models.Model):
    """Модель города."""

    name = models.CharField(max_length=100,
                            null=False,
                            blank=False,
                            verbose_name='Название города')

    class Meta:
        """Русское название модели."""

        verbose_name = 'Город'
        verbose_name_plural = 'Города'

    def __str__(self):
        """Возвращает название города."""
        return self.name


class Warehouse(models.Model):
    """Модель склада."""

    name = models.CharField(
        max_length=254,
        null=False,
        verbose_name='Склад'
    )

    class Meta:
        """Русское название модели."""

        verbose_name = 'Склад'
        verbose_name_plural = 'Склады'

    def __str__(self):
        """Возвращает название поля."""
        return self.name


class Store(models.Model):
    """Модель магазина салона."""

    name = models.CharField(
        max_length=254,
        null=False,
        verbose_name='Название магазина'
    )
    info = models.TextField(
        null=True,
        blank=True,
        verbose_name='Информация о салоне'
    )
    city = models.ForeignKey(
        City,
        related_name='cities',
        blank=False,
        on_delete=models.DO_NOTHING,
        verbose_name='Город'
    )

    class Meta:
        """Русское название модели."""

        verbose_name = 'Магазин'
        verbose_name_plural = 'Магазины'

    def __str__(self):
        """Возвращает название поля."""
        return self.name


class User(AbstractUser):
    """Дополненная модель пользователя."""

    work_position = models.ForeignKey(
        WorkPosition,
        on_delete=models.DO_NOTHING,
        null=True,
        verbose_name='Должность'
    )
    store = models.ManyToManyField(
        Store,
        related_name='stores'
    )
    groups = models.ManyToManyField(
        Group,
        related_name='custom_user_set',  # Уникальное имя для related_name
        blank=True,
        help_text='The groups this user belongs to. A user will get all '
                  'permissions granted to each of their groups.',
        verbose_name='groups',
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name='custom_user_permission_set',
        # Уникальное имя для related_name
        blank=True,
        help_text='Specific permissions for this user.',
        verbose_name='user permissions',
    )


class ProductCategory(models.Model):
    """Модель связывающая товар и категории связью многие-ко-многим."""

    id = models.CharField(
        primary_key=True,
        max_length=18,
        null=False,
        verbose_name='Код'
    )
    name = models.CharField(
        max_length=128,
        unique=True,
        verbose_name='Название категории'
    )

    class Meta:
        """Русское название модели."""

        verbose_name = 'Категория',
        verbose_name_plural = 'Категории'

    def __str__(self):
        """Возвращает название поля."""
        return self.name


class Product(models.Model):
    """Модель товара."""

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
        verbose_name='Класс комнаты',
        default='Нет класса'
    )

    class Meta:
        """Русское название модели."""

        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'

    def __str__(self):
        """Возвращает название поля."""
        return self.name


class WarehouseProduct(models.Model):
    """Связующая модель для таблиц Склад и Товар."""

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
        """Добавляет уникальное поле в качестве сочетания склада и товара."""

        constraints = [
            models.UniqueConstraint(fields=['warehouse', 'product'],
                                    name='unique_warehouse_product')
        ]
        verbose_name = 'Продукт на складе'
        verbose_name_plural = 'Продукты на складе'


class StoreProduct(models.Model):
    """Связующая модель для таблиц Магазин и Товар."""

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

    @property
    def deviation(self):
        """Добавляет новое свойство. Вычисляемое поле"""
        if self.plan_exhibition is not None and self.fact_exhibition is not None:
            return self.fact_exhibition - self.plan_exhibition
        return 0

    def __str__(self):
        """Возвращает название товара и магазина."""
        return f'{self.product.name} - {self.store.name}'

    class Meta:
        """Русское название модели."""

        constraints = [
            models.UniqueConstraint(fields=['store', 'product'],
                                    name='unique_store_product')
        ]
        verbose_name = 'Мебельный салон'
        verbose_name_plural = 'Мебельные салоны'


class Comment(models.Model):
    """Модель комментария."""

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
        verbose_name='Статус комментария'
    )

    class Meta:
        """Русское название модели."""

        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'

    def __str__(self):
        """Возвращает название поля."""
        return self.text
