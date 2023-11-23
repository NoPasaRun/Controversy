from django.contrib import admin
from .models import User, Order, Size, Product


admin.site.register(User)
admin.site.register(Order)
admin.site.register(Size)
admin.site.register(Product)
