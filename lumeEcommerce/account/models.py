from django import forms
from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class CustomerProfile(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='customer_profile'  # Define explicit related_name
    )
    supports_flamengo = models.BooleanField(default=False, verbose_name='Sou fã do Mengão')
    watches_one_piece = models.BooleanField(default=False, verbose_name='Tenho pôster de OP no quarto')
    is_from_sousa = models.BooleanField(default=False, verbose_name='Sou de Sousa')

    def has_discount(self):
        # Discount condition
        return self.supports_flamengo or self.watches_one_piece or self.is_from_sousa

    def __str__(self):
        return f"Profile for {self.user.username}"