# Generated by Django 4.2 on 2023-05-02 09:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_alter_product_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='image',
            field=models.ImageField(default='uploads/default_image_1.png', max_length=255, upload_to='uploads/', verbose_name='Фото товара'),
        ),
        migrations.AlterField(
            model_name='product',
            name='unit_of_measurement_of_volume',
            field=models.CharField(choices=[('kg', 'кг'), ('g', 'гр'), ('l', 'л'), ('ml', 'мл'), ('sachet', 'cаше'), ('portion', 'порции'), ('pairs', 'пар')], max_length=100, verbose_name='Выберите единицу измерения объёма продукта'),
        ),
    ]
