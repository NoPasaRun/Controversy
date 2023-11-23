# Generated by Django 4.2.7 on 2023-11-23 18:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('server', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='price',
            field=models.PositiveSmallIntegerField(default=2, verbose_name='Цена'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='product',
            name='image',
            field=models.FileField(upload_to='images', verbose_name='Изображение'),
        ),
    ]
