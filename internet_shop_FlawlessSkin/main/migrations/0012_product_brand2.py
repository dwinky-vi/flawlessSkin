# Generated by Django 4.2 on 2023-05-14 13:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0011_productbrand'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='brand2',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='main.productbrand', verbose_name='Бренд'),
        ),
    ]
