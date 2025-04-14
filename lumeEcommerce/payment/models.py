from django.db import models
from django.contrib.auth.models import User
from store.models import Product

class Seller(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    commission_rate = models.DecimalField(max_digits=5, decimal_places=2, default=5.00)
    hire_date = models.DateField(auto_now_add=True)
    
    def __str__(self):
        return f"Vendedor: {self.user.first_name} {self.user.last_name}"

class PaymentMethod(models.Model):
    PAYMENT_TYPES = (
        ('credit', 'Cartão de Crédito'),
        ('debit', 'Cartão de Débito'), 
        ('pix', 'PIX'),
        ('boleto', 'Boleto'),
        ('berries', 'Berries'),
    )
    
    PAYMENT_STATUS = (
        ('pending', 'Pendente'),
        ('confirmed', 'Confirmado'),
        ('rejected', 'Rejeitado'),
    )
    
    type = models.CharField(max_length=20, choices=PAYMENT_TYPES)
    status = models.CharField(max_length=20, choices=PAYMENT_STATUS, default='pending')
    transaction_id = models.CharField(max_length=100, blank=True, null=True)
    payment_date = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.get_type_display()} - {self.get_status_display()}"

class Order(models.Model):
    full_name = models.CharField(max_length=300)
    email = models.EmailField(max_length=255)
    shipping_address = models.TextField(max_length=10000)
    amount_paid = models.DecimalField(max_digits=8, decimal_places=2)
    discount_amount = models.DecimalField(max_digits=8, decimal_places=2, default=0.00)
    date_ordered = models.DateTimeField(auto_now_add=True)
    
    # Foreign Keys
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    seller = models.ForeignKey(Seller, on_delete=models.SET_NULL, null=True)
    payment_method = models.OneToOneField(PaymentMethod, on_delete=models.CASCADE, null=True)
    
    def __str__(self):
        return 'Order - #' + str(self.id)
    
    class Meta:
        indexes = [
            models.Index(fields=['date_ordered']),
            models.Index(fields=['seller']),
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


class OrderItem(models.Model):

    # Foreign Key
    order = models.ForeignKey(Order, on_delete=models.CASCADE, null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True)

    quantity = models.PositiveBigIntegerField(default=1)
    price = models.DecimalField(max_digits=8, decimal_places=2)

    # Foreign Key
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return 'Order Item - #' + str(self.id)
    
    class Meta:
        indexes = [
            models.Index(fields=['product', 'order']),
        ]
        constraints = [
            models.CheckConstraint(
                check=models.Q(quantity__gt=0),
                name='quantity_greater_than_zero'
            )
        ]
