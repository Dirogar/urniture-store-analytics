from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser

User = get_user_model()

DEFAULT_AREA = 0


class Shops(models.Model):
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
    members = models.ManyToManyField(User, related_name='shops')

    class Meta:
        verbose_name = 'Мебельный салон'
        verbose_name_plural = 'Мебельные салоны'

    def __str__(self):
        return self.name


class Comment(models.Model):
    text = models.TextField(verbose_name='Комментарий')
    shop = models.ForeignKey(
        Shops,
        on_delete=models.CASCADE,
        verbose_name='Мебельный салон',
        null=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)


