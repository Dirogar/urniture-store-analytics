from django import forms
from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.admin.widgets import FilteredSelectMultiple

from django.contrib.auth.models import User
from .models import Store, Product, Warehouse, ProductCategory

User = get_user_model()


class StoreAdminForm(forms.ModelForm):
    class Meta:
        model = Store
        fields = '__all__'

    users = forms.ModelMultipleChoiceField(
        queryset=User.objects.all(),
        required=False,
        widget=FilteredSelectMultiple(
            verbose_name='Пользователи',
            is_stacked=False
        ),
        label=''
    )


@admin.register(Store)
class StoreAdmin(admin.ModelAdmin):
    form = StoreAdminForm
    list_display = ('name',)
    search_fields = ('name',)


admin.site.register(Warehouse)
# admin.site.register(Store)
admin.site.register(Product)
admin.site.register(ProductCategory)
