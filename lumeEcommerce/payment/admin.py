from django.contrib import admin
from .models import Seller, PaymentMethod, ShippingAddress, Order, OrderItem
# Register your models here.

admin.site.register(Seller)
admin.site.register(PaymentMethod)
admin.site.register(ShippingAddress)
admin.site.register(Order)
admin.site.register(OrderItem)
