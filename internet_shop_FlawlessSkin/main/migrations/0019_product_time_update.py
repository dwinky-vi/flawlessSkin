# Generated by Django 4.2.1 on 2023-05-23 18:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0018_product_slug'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='time_update',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
