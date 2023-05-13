from django.db import models

from users.models import User


# Create your models here.
# models == модели == таблицы
# миграция -- перенос структуры модели на структуру БД
# Команды:
#     makemigrations - создание новых миграций
#     migrate - применение миграции

# QuerySet - это набор запросов, который представляется собой набор объектов из БД
# • create() - создает объект из БД
# • get() - возвращает объект из БД
# • all() - возвращает список всех объектов из БД
# • filter() - возвращает список объектов из БД по определенному признаку

class ProductCategory(models.Model):
	name = models.CharField("Название", max_length=128, unique=True)
	description = models.TextField("Описание", null=True, blank=True)
	
	def __str__(self):
		return self.name
	
	class Meta:
		verbose_name = "Категория товара"
		verbose_name_plural = "Категории товаров"


class Product(models.Model):
	units_of_measurement = (
		('kg', 'кг'),
		('g', 'гр'),
		('l', 'л'),
		('ml', 'мл'),
		('sachet', 'cаше'),
		('portion', 'порции'),
		('pairs', 'пар'),
	)
	title = models.CharField("Название товара", max_length=255, default="")
	image = models.ImageField("Фото товара", upload_to="uploads/products/", default="uploads/default_image_1.png",
							  max_length=255)
	description = models.TextField("Описание", help_text="Укажите подробное описание товара")
	structure = models.TextField("Состав", help_text="Укажите компоненты через запятую (,)")
	price = models.IntegerField("Цена", help_text="Введите число без пробелов")
	country_manufacture = models.CharField("Производство", max_length=50, help_text="Страна производства товара")
	brand = models.CharField("Бренд", max_length=50)
	volume = models.PositiveIntegerField("Объём продукта")
	unit_of_measurement_of_volume = models.CharField("Выберите единицу измерения объёма продукта", max_length=100,
													 choices=units_of_measurement)
	date = models.DateField("Дата поступления товара")
	quantity = models.PositiveIntegerField("Количество штук", default=0)
	#     есть 3 вида удаления:
	#     CASCADE (при удаление одной категории, удалятся все товары, которые принадлежат данной категории)
	#     PROTECT (нельзя будет удалить категорию, пока есть товары принадлежащие данной категории)
	#     SET_DEFAULT (если удаляется категория, то в эту переменную ставится значение по умолчанию)
	
	category = models.ForeignKey(to=ProductCategory, on_delete=models.PROTECT, default=1)
	
	def __str__(self):
		return self.title
	
	class Meta:
		verbose_name = "Товар"
		verbose_name_plural = "Товары"

	# ИЗБРАННОЕ
class Favourites(models.Model):
	# каскадное удаление. если удалился пользователь, то удалятся его избранные товары
	user = models.ForeignKey(to=User, on_delete=models.CASCADE, null=True)
	# удалился продукт -> удалось из избранных
	product = models.ForeignKey(to=Product, on_delete=models.CASCADE)
	# автоматически заполняется при создании объекта
	created_timestamp = models.DateTimeField(auto_now_add=True)
	
	def __str__(self):
		return f"пользователь: {self.user.username} | продукт: {self.product.title}"

	class Meta:
		verbose_name = "Избранное"
		verbose_name_plural = "Избранные"


class CartQuerySet(models.QuerySet):
	# итоговая сумма всех товаров в корзине
	def total_amount(self):
		return sum(cart.sum() for cart in self)
		
	# количество всех товаров в корзине
	def total_quantity(self):
		return sum(cart.quantity for cart in self)


	# КОРЗИНА
class Cart(models.Model):
	# каскадное удаление. если удалился пользователь, то удаляется его корзина
	user = models.ForeignKey(verbose_name="Пользователь", to=User, on_delete=models.CASCADE, null=True)
	# удалился продукт -> удалится корзина
	product = models.ForeignKey(verbose_name="Товар", to=Product, on_delete=models.CASCADE)
	# количество добавленых единиц в корзине
	quantity = models.PositiveSmallIntegerField("Количество добавленных единиц")
	# автоматически заполняется при создании объекта
	created_timestamp = models.DateTimeField(auto_now_add=True)
	
	def __str__(self):
		return f"пользователь: {self.user.username} | продукт: {self.product.title}"
	
	class Meta:
		verbose_name = "Корзина"
		verbose_name_plural = "Корзины"
	
	# сумма товаров одного вида
	def sum_price(self):
		return self.quantity * self.product.price
	
	# итоговая сумма всех товаров в корзине
	def total_amount(self):
		carts = Cart.objects.filter(user=self.user)
		return sum(cart.sum_price() for cart in carts)
	
	# количество всех товаров в корзине
	def total_quantity(self):
		carts = Cart.objects.filter(user=self.user)
		return sum(cart.quantity for cart in carts)

	objects = CartQuerySet.as_manager()


