from django import forms
from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class CustomerProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    supports_flamengo = models.BooleanField(default=False, name='Sou fã do Mengão')
    watches_one_piece = models.BooleanField(default=False, name='Tenho pôster de OP no quarto')
    city = forms.ChoiceField(choices=[('Sousa', 'Sousa'), ('Other', 'Other')])

    def has_discount(self):
        # Discount condition
        return self.supports_flamengo or self.watches_one_piece or self.city.strip().lower() == "sousa"

    def __str__(self):
        return f"Profile for {self.user.username}"