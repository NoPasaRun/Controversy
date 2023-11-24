import uuid

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
        if self.number == 38:
            return 'XXS'
        elif self.number == 40:
            return 'XS'
        elif self.number == 42:
            return 'S'
        elif self.number in [44, 45, 46]:
            return 'M'
        elif self.number in [48, 49, 50]:
            return 'L'
        elif self.number == '52':
            return 'XL'
        elif self.number in [54, 55, 56]:
            return 'XXL'
        elif self.number == '58':
            return '3XL'
        else:
            return None
     
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
    price = models.PositiveSmallIntegerField(
        verbose_name='Цена'
    )
    image = models.FileField( 
        verbose_name='Изображение', 
        upload_to='images' 
    ) 
    description = models.TextField( 
        verbose_name='Описание' 
    ) 
    uuid = models.UUIDField( 
        verbose_name='Код товара', 
        default=uuid.uuid4, 
        editable=False, 
        unique=True
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
        ('card', 'картой')
    ) 
    STATUSES = ( 
        ('paid', 'оплачено'), 
        ('packed', 'упаковано'),
        ('on_the_way', 'в пути'), 
        ('delivered', 'доставлено'),
        ('waiting', 'ожидает в пункте выдачи')
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
    city = models.CharField(
        verbose_name='Город',
        max_length=64,
        blank=True
    )
    address = models.CharField(
        verbose_name='Адрес',
        max_length=128,
        blank=True
    )
    products = models.ManyToManyField(
        Product,
        related_query_name="orders",
        verbose_name="Товары"
    )
 
    def __str__(self): 
        return str(self.id) 
     
    class Meta: 
        verbose_name = 'Заказ' 
        verbose_name_plural = 'Заказы'
