from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django import forms
from django.forms.widgets import PasswordInput, TextInput


# Registration form
class CreateUserForm(UserCreationForm):

    username = forms.CharField(
        label="Usuário",
        help_text="Obrigatório. Máximo de 150 caracteres. Apenas letras, números e @/./+/-/_."
    )
    email = forms.EmailField(label="E-mail")
    password1 = forms.CharField(
        label="Senha",
        widget=forms.PasswordInput,
        help_text=(
            "<ul>"
            "<li>Sua senha não pode ser muito parecida com suas outras informações pessoais.</li>"
            "<li>Sua senha deve conter pelo menos 8 caracteres.</li>"
            "<li>Sua senha não pode ser uma senha comumente utilizada.</li>"
            "<li>Sua senha não pode ser inteiramente numérica.</li>"
            "</ul>"
        )
    )
    password2 = forms.CharField(
        label="Confirmação de senha",
        widget=forms.PasswordInput,
        help_text="Digite a mesma senha informada anteriormente, para verificação."
    )

    class Meta:

        model = User
        fields = ['username', 'email', 'password1', 'password2']

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
    username = forms.CharField(widget=TextInput(), label='Usuário')
    password = forms.CharField(widget=PasswordInput(), label='Senha')


# Update form
class UpdateUserForm(forms.ModelForm):
    password = None

    class Meta:

        model = User
        fields = ['username', 'email']
        exclude = ['password1', 'password2']

    username = forms.CharField(
        label="Usuário",
        help_text="Obrigatório. Máximo de 150 caracteres. Apenas letras, números e @/./+/-/_."
    )
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
