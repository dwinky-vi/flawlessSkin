# Generated by Django 4.2 on 2023-04-28 11:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_alter_product_options_product_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='image',
            field=models.ImageField(default='uploads/default_image_2', max_length=255, null=True, upload_to='uploads/', verbose_name='Фото товара'),
        ),
    ]
