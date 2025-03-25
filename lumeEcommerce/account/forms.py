from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django import forms
from django.forms.widgets import PasswordInput, TextInput


# Registration form
class CreateUserForm(UserCreationForm):
    class Meta:

        model = User
        fields = ['username', 'email', 'password1', 'password2']

    email = forms.EmailField(label="E-mail")


    def __init__(self, *args, **kwargs):
        super(CreateUserForm, self).__init__(*args, **kwargs)

    # Email validation
    def clean_email(self):
        email = self.cleaned_data.get('email')

        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('Já existe uma conta com este email!')

        if len(email) >= 350:
            raise forms.ValidationError('Email inválido: muito longo!')

        return email


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
