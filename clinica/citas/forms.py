from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import authenticate  # Asegúrate de importar authenticate

class RegistroForm(forms.ModelForm):
    username = forms.CharField(label='Nombre de usuario', max_length=150, error_messages={'required': _('Este campo es obligatorio.')})
    password = forms.CharField(label='Contraseña', widget=forms.PasswordInput, error_messages={'required': _('Este campo es obligatorio.')})
    password_confirmation = forms.CharField(label='Confirmar Contraseña', widget=forms.PasswordInput, error_messages={'required': _('Este campo es obligatorio.')})
    email = forms.EmailField(label='Correo electrónico', error_messages={'required': _('Este campo es obligatorio.'), 'invalid': _('Ingresa un correo electrónico válido.')})

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password_confirmation = cleaned_data.get("password_confirmation")

        if password and password_confirmation:
            if password != password_confirmation:
                raise ValidationError(_("Las contraseñas no coinciden."))

        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])  # Encriptar la contraseña
        if commit:
            user.save()
        return user


class LoginForm(forms.Form):
    run = forms.CharField(label='RUN', max_length=12)
    password = forms.CharField(label='Contraseña', widget=forms.PasswordInput)
    additional_data = forms.CharField(label='Numero de documento')  # Campo adicional
    auth_code = forms.CharField(label='Código de Autenticación', max_length=6)  # Código para 2FA

    def clean(self):
        cleaned_data = super().clean()
        run = cleaned_data.get("run")
        password = cleaned_data.get("password")
        auth_code = cleaned_data.get("auth_code")

        if run and password and auth_code:
            user = authenticate(username=run, password=password)  # Cambiado a username
            if user is None:
                raise forms.ValidationError("Credenciales incorrectas.")

            # Aquí debes verificar el código de autenticación
            if not self.verify_auth_code(user, auth_code):
                raise forms.ValidationError("Código de autenticación incorrecto.")
        return cleaned_data

    def verify_auth_code(self, user, auth_code):
        # Lógica para verificar el código de autenticación
        return auth_code == "123456"  # Ejemplo de código estático
