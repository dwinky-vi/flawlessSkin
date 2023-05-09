from django.contrib import admin
from .models import Product
from main.models import ProductCategory, Cart, Favourites

# этот файл отвечает за регистрацию таблиц
# Чтобы таблица отображалась в админке
# Register your models here.
admin.site.register(Product)
admin.site.register(ProductCategory)
admin.site.register(Cart)
admin.site.register(Favourites)
