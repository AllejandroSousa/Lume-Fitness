from django.db import models
from django.contrib.auth.models import User
from store.models import Product
# Create your models here.

# Payment methods options
PAYMENT_METHOD_CHOICES = [
    ('PIX', 'PIX'),
    ('Credit Card', 'Credit Card'),
    ('Boleto', 'Boleto'),
]

# Order status options
ORDER_STATUS_CHOICES = [
    ('Waiting for Confirmation', 'Waiting for Confirmation'),
    ('Confirmed', 'Confirmed'),
    ('Cancelled', 'Cancelled'),
]

class ShippingAddress(models.Model):

    full_name = models.CharField(max_length=300)
    email = models.EmailField(max_length=255)
    address1 = models.CharField(max_length=300)
    address2 = models.CharField(max_length=300, null=True, blank=True)
    city = models.CharField(max_length=255)
    state = models.CharField(max_length=255)
    zipcode = models.CharField(max_length=255)

    # Foreign Key
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, null=True, blank=True)

    class Meta:

        verbose_name_plural = 'Shipping address'

    def __str__(self):
        return 'Shipping address - ' + str(self.id)


class Order(models.Model):
    full_name = models.CharField(max_length=100)
    customer = models.ForeignKey(User, on_delete=models.CASCADE, related_name="orders")
    email = models.EmailField()
    amount_paid = models.DecimalField(max_digits=10, decimal_places=2)
    shipping_address = models.TextField(max_length=10000)
    order_date = models.DateTimeField(auto_now_add=True)
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHOD_CHOICES)
    order_status = models.CharField(max_length=30, choices=ORDER_STATUS_CHOICES, default='Pendent')
    seller = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name="sales")

    def __str__(self):
        return f"Order #{self.pk} by {self.customer.username}"

    @property
    def total(self):
        return sum(item.subtotal for item in self.items.all())


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    quantity = models.PositiveIntegerField()

    @property
    def subtotal(self):
        return self.product.price * self.quantity

