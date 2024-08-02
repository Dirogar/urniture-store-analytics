from django import forms
from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.admin.widgets import FilteredSelectMultiple
from django.utils.translation import gettext, gettext_lazy as _

from django.contrib.auth.models import User
from .models import Store, Product, Warehouse, ProductCategory, City, User


class CustomUserCreationForm(UserCreationForm):
    store = forms.ModelMultipleChoiceField(
        queryset=Store.objects.all(),
        required=False,
        widget=FilteredSelectMultiple(
            verbose_name='Магазины',
            is_stacked=False
        ),
    )

    class Meta:
        model = User
        fields = ('username', 'email', 'work_position', 'password1', 'password2', 'store')


class CustomUserChangeForm(UserChangeForm):
    store = forms.ModelMultipleChoiceField(
        queryset=Store.objects.all(),
        required=False,
        widget=FilteredSelectMultiple(
            verbose_name='Магазины',
            is_stacked=False
        ),
    )
    class Meta:
        model = User
        fields = ('username', 'email', 'work_position', 'password', 'store')


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    list_display = ('username', 'email', 'work_position')

    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('email', 'work_position', 'store')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'work_position', 'password1', 'password2'),
        }),
    )

    search_fields = ('username', 'email')
    ordering = ('username',)



admin.site.register(Warehouse)
admin.site.register(Product)
admin.site.register(ProductCategory)
admin.site.register(City)
admin.site.register(Store)


