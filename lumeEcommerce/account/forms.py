from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django import forms
from django.forms.widgets import PasswordInput, TextInput

from .models import CustomerProfile


# Registration form
class CreateUserForm(UserCreationForm):
    email = forms.EmailField(required=True, label='E-mail')
    supports_flamengo = forms.BooleanField(
        required=False,
        label='Sou fã do Mengão',
    )
    watches_one_piece = forms.BooleanField(
        required=False,
        label='Tenho pôster de OP no quarto',
    )
    is_from_sousa = forms.BooleanField(
        required=False,
        label='Sou de Sousa',
    )

    def __init__(self, *args, **kwargs):
        super(CreateUserForm, self).__init__(*args, **kwargs)

    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'password1',
            'password2',
            'supports_flamengo',
            'watches_one_piece',
            'is_from_sousa'
        ]

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
            CustomerProfile.objects.update_or_create(
                user=user,
                defaults={
                    'supports_flamengo': self.cleaned_data['supports_flamengo'],
                    'watches_one_piece': self.cleaned_data['watches_one_piece'],
                    'is_from_sousa': self.cleaned_data['is_from_sousa'],
                }
            )
        return user


# Login form
class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=TextInput())
    password = forms.CharField(widget=PasswordInput(), label='Senha')


# Update form
class UpdateUserForm(forms.ModelForm):
    password = None

    class Meta:

        model = User
        fields = ['username', 'email']
        exclude = ['password1', 'password2']

    email = forms.EmailField(label="E-mail")

    def __init__(self, *args, **kwargs):
        super(UpdateUserForm, self).__init__(*args, **kwargs)

    # Email validation
    def clean_email(self):
        email = self.cleaned_data.get('email')

        if User.objects.filter(email=email).exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError('Já existe uma conta com este email!')

        if len(email) >= 350:
            raise forms.ValidationError('Email inválido: muito longo!')

        return email
