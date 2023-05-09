from django.db import models
# используем существующую модель, чтобы расширить её
from django.contrib.auth.models import AbstractUser

# Create your models here.

class User(AbstractUser):
	# работа с изображение
	image = models.ImageField("Аватарка", upload_to='uploads/users_images/', blank=True, null=True)
	phone = models.CharField("Номер телефона", max_length=20, blank=True, null=True)
	address = models.CharField("Адрес доставки", max_length=255, blank=True, null=True)
