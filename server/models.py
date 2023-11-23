import re

from django.db import models 
from django.contrib.auth.models import AbstractUser 
from django.core.validators import RegexValidator 
 
 
class User(AbstractUser): 
 
    phoneNumberRegex = RegexValidator(regex=r"^\+?1?\d{8,15}$") 
    phone_number = models.CharField( 
        verbose_name='Номер телефона',  
        validators=[phoneNumberRegex],  
        max_length=16,  
        blank=True,  
        null=True 
    ) 
     
    def __str__(self): 
        return self.username 
     
    class Meta: 
        verbose_name = 'Пользователь' 
        verbose_name_plural = 'Пользователи' 
 
 
class Size(models.Model): 
 
    number = models.PositiveSmallIntegerField( 
        verbose_name='Номер' 
    ) 
 
    @property 
    def name(self): 
        match str(self.number):
            case '38':
                return 'XXS'
            case '40':
                return 'XS'
            case '42':
                return 'S'
            case size if re.match(r"[44-46]"):
                return 'M'
            case size if re.match(r"[48-50]"):
                return 'L'
            case '52':
                return 'XL'
            case size if re.match(r"[54-56]"):
                return 'XXL'
            case '58':
                return '3XL'
            case _:
                return 'Размер не подходит под Американские стандарты'
     
    def __str__(self): 
        return str(self.number) 
     
    class Meta: 
        verbose_name = 'Размер' 
        verbose_name_plural = 'Размеры' 
 
 
class Product(models.Model): 
 
    title = models.CharField( 
        verbose_name='Название', 
        max_length=32 
    ) 
    image = models.FileField( 
        verbose_name='Изображение', 
        upload_to='images/product' 
    ) 
    description = models.TextField( 
        verbose_name='Описание' 
    ) 
    uuid = models.UUIDField( 
        verbose_name='Код товара', 
        unique=True, 
        auto_created=True 
    ) 
    sizes = models.ManyToManyField( 
        verbose_name='Доступные размеры',
        to=Size
    ) 
    quantity = models.PositiveSmallIntegerField( 
        verbose_name='Осталось на складе' 
    ) 
 
    def __str__(self): 
        return self.title 
     
    class Meta: 
        verbose_name = 'Товар' 
        verbose_name_plural = 'Товары' 
 
 
class Order(models.Model): 
 
    user = models.ForeignKey( 
        'User', 
        verbose_name='Заказчик', 
        on_delete=models.CASCADE 
    ) 
 
    DELIVERY_TYPES = ( 
        ('express', 'быстрая'), 
        ('default', 'обычная'), 
        ('issue_point', 'пункт выдачи') 
    ) 
    PAYMENT_TYPES = ( 
        ('cash', 'наличными'), 
        ('card', 'картой'), 
        ('anal', 'очком понеделки') 
    ) 
    STATUSES = ( 
        ('paid', 'оплачено'), 
        ('packed', 'упаковано (ебало понеделки)'), 
        ('on_the_way', 'в пути'), 
        ('delivered', 'доставлено (как двоечка в бороду понеделки)'), 
        ('waiting', 'ожидает в пункте выдачи (по ебалу понеделке)') 
    ) 
 
    delivery_type = models.CharField( 
        verbose_name='Способ доставки', 
        choices=DELIVERY_TYPES, 
        max_length=12 
    ) 
    payment_type = models.CharField( 
        verbose_name='Способ оплаты', 
        choices=PAYMENT_TYPES, 
        max_length=15 
    ) 
    status = models.CharField( 
        verbose_name='Статус заказа', 
        choices=STATUSES, 
        max_length=44 
    ) 
 
    def __str__(self): 
        return str(self.id) 
     
    class Meta: 
        verbose_name = 'Заказ' 
        verbose_name_plural = 'Заказы'
