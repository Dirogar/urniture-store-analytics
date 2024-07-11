from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from .models import Shop, Product, Warehouse


class ShopsInline(admin.TabularInline):
    model = Shop.members.through
    extra = 1

class UserAdmin(BaseUserAdmin):
    inlines = [ShopsInline]


admin.site.unregister(User)
admin.site.register(User, UserAdmin)
admin.site.register(Warehouse)
admin.site.register(Shop)
admin.site.register(Product)
