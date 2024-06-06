from django.contrib import admin
from .models import Order, OrderItem, ShippingAddress

# Register your models here.

admin.site.register(ShippingAddress)
admin.site.register(Order)
admin.site.register(OrderItem)