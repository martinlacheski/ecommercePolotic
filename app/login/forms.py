from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import TextInput, PasswordInput


class UserCreationForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['first_name'].widget.attrs['autofocus'] = True

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2',)
        widgets = {
            'username': TextInput(
                attrs={
                    'placeholder': 'Ingrese un nombre de Usuario',
                }
            ),
            'first_name': TextInput(
                attrs={
                    'placeholder': 'Ingrese sus nombres',
                }
            ),
            'last_name': TextInput(
                attrs={
                    'placeholder': 'Ingrese sus apellidos',
                }
            ),
            'email': TextInput(
                attrs={
                    'placeholder': 'Ingrese un correo electrónico válido',
                    'style': 'width: 100%'
                }
            ),
            'password1': PasswordInput(render_value=True,
                                       attrs={
                                           'placeholder': 'Ingrese una contraseña',
                                           'style': 'width: 100%'
                                       }
                                       ),
            'password2': PasswordInput(render_value=True,
                                       attrs={
                                           'placeholder': 'Ingrese nuevamente la contraseña',
                                           'style': 'width: 100%'
                                       }
                                       ),
        }
