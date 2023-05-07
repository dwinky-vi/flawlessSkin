from django.db import models
# используем существующцю модель, чтобы расширить её
from django.contrib.auth.models import AbstractUser

# Create your models here.

class User(AbstractUser):
	# работа с изображение
	image = models.ImageField(upload_to='users_images', blank=True, null=True)
	phone = models.CharField(max_length=20, blank=True, null=True)
	address = models.CharField(max_length=255, blank=True, null=True)
	# username =
