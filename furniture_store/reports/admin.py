from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from .models import Store, Product, Warehouse, ProductCategory


admin.site.register(Warehouse)
admin.site.register(Store)
admin.site.register(Product)
admin.site.register(ProductCategory)
