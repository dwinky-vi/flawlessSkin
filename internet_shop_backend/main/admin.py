from django.contrib import admin
from .models import Product

# этот файл отвечает за регистрацию таблиц
# Чтобы таблица отображалась в админке
# Register your models here.
admin.site.register(Product)
