from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from .models import Store, Product, Warehouse


admin.site.unregister(User)
admin.site.register(Warehouse)
admin.site.register(Store)
admin.site.register(Product)
