# Generated by Django 4.2 on 2023-05-14 12:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0009_alter_cart_options_alter_productcategory_options_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='favourites',
            options={'verbose_name': 'Избранное', 'verbose_name_plural': 'Избранные'},
        ),
    ]
