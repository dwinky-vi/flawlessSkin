from django.db import models
# используем существующцю модель, чтобы расширить её
from django.contrib.auth.models import AbstractUser

# Create your models here.

class User(AbstractUser):
#     работа с изобращение
    image = models.ImageField(upload_to='users_images', blank=True, null=True)
