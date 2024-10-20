from django import forms

class LoginForm(forms.Form):
    run = forms.CharField(max_length=12, label="RUN")
    numero_documento = forms.IntegerField(label="Número de Documento")
    password = forms.CharField(widget=forms.PasswordInput, label="Contraseña")
    codigo_2fa = forms.CharField(max_length=6, label="Código 2FA")

class RegistroForm(forms.Form):
    nombre_usuario = forms.CharField(max_length=100, label="Nombre de Usuario")
    numero_celular = forms.IntegerField(label="Número de Celular")
    run = forms.CharField(max_length=12, label="RUN")
    numero_documento = forms.IntegerField(label="Número de Documento")
    password = forms.CharField(widget=forms.PasswordInput, label="Contraseña")
    confirm_password = forms.CharField(widget=forms.PasswordInput, label="Confirmar Contraseña")
    codigo_2fa = forms.CharField(max_length=6, label="Código 2FA")