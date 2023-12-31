# Generated by Django 4.2.7 on 2023-11-24 08:12

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('server', '0003_alter_product_uuid'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='address',
            field=models.CharField(default='', max_length=128, verbose_name='Адрес'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='order',
            name='city',
            field=models.CharField(default='', max_length=64, verbose_name='Город'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='order',
            name='products',
            field=models.ManyToManyField(related_query_name='orders', to='server.product', verbose_name='Товары'),
        ),
        migrations.AlterField(
            model_name='order',
            name='payment_type',
            field=models.CharField(choices=[('cash', 'наличными'), ('card', 'картой')], max_length=15, verbose_name='Способ оплаты'),
        ),
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('paid', 'оплачено'), ('packed', 'упаковано'), ('on_the_way', 'в пути'), ('delivered', 'доставлено'), ('waiting', 'ожидает в пункте выдачи')], max_length=44, verbose_name='Статус заказа'),
        ),
        migrations.AlterField(
            model_name='product',
            name='uuid',
            field=models.UUIDField(default=uuid.uuid4, editable=False, unique=True, verbose_name='Код товара'),
        ),
    ]
