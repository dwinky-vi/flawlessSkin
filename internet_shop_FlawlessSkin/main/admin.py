from django.contrib import admin
from .models import Product
from main.models import ProductCategory, ProductBrand, Cart, Favourites, Order

# этот файл отвечает за регистрацию таблиц
# Чтобы таблица отображалась в админке
# Register your models here.
admin.site.register(ProductCategory)
admin.site.register(ProductBrand)
admin.site.register(Cart)
admin.site.register(Favourites)
admin.site.register(Order)


class ProductAdmin(admin.ModelAdmin):
	# search_fields = ("title", )
	prepopulated_fields = {"slug": ("title",)}  # автоматически заполнять поле slug на основе поля title
	


admin.site.register(Product, ProductAdmin)
# admin.site.register(ProductAdmin)
