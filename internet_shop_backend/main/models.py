from django.db import models

# Create your models here.

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
	image = models.ImageField("Фото товара", upload_to="uploads/", default="uploads/default_image_1.png", max_length=255)
	description = models.TextField("Описание", help_text="Укажите подробное описание товара")
	structure = models.TextField("Состав", help_text="Укажите компоненты через запятую (,)")
	price = models.IntegerField("Цена", help_text="Введите только число")
	country_manufacture = models.CharField("Производство", max_length=50, help_text="Страна производства товара")
	brand = models.CharField("Бренд", max_length=50)
	volume = models.IntegerField("Объём продукта")
	unit_of_measurement_of_volume = models.CharField("Выберите единицу измерения объёма продукта", max_length=100, choices=units_of_measurement)
	date = models.DateField("Дата поступления товара")
	
	def __str__(self):
		return self.title

	class Meta:
		verbose_name = "Товар"
		verbose_name_plural = "Товары"

# КОРЗИНА
class Cart(models.Model):
	# каскадное удаление. если удалился пользователь, то удаляется его корзина
	# user = models.ForeignKey(to=User, on_delete=models.CASCADE)
	# удалился продукт -> удалить корзину
	product = models.ForeignKey(to=Product, on_delete=models.CASCADE)
	# количество добавленых единиц в корзине
	quantity = models.PositiveSmallIntegerField(default=0)
	# автоматически заполняется при создании объекта
	created_timestamp = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		# return f"корзина для {self.user.email} | продукт: {self.product.name}"
		return f"корзина для user | продукт: {self.product.name}"
