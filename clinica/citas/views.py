from django.shortcuts import render, redirect
from .models import Usuario
from .forms import RegistroForm, LoginForm
from django.contrib.auth import login, authenticate
from django.contrib import messages  # Para mostrar mensajes de error

def registro_web(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        form = RegistroForm(request.POST)
        if form.is_valid():
            usuario = form.save(commit=False)
            usuario.set_password(form.cleaned_data['password'])
            usuario.save()
            messages.success(request, "Registro exitoso. Puedes iniciar sesión.")
            return redirect('login')
    else:
        form = RegistroForm()
    return render(request, "register.html", {'form': form})


def login_web(request):
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            numero_documento = form.cleaned_data['additional_data']  # Asegúrate de que este campo se llama así en tu formulario
            password = form.cleaned_data['password']
            auth_code = form.cleaned_data['auth_code']

            try:
                # Busca el usuario por el número de documento
                usuario = Usuario.objects.get(numero_documento=numero_documento)
                # Verifica la contraseña
                if usuario.check_password(password):
                    if form.verify_auth_code(usuario, auth_code):  # Asegúrate de que esta función esté definida
                        login(request, usuario)
                        return redirect('home')
                    else:
                        messages.error(request, "Código de autenticación incorrecto.")
                else:
                    messages.error(request, "Credenciales incorrectas.")
            except Usuario.DoesNotExist:
                messages.error(request, "Credenciales incorrectas.")  # Usuario no encontrado
    else:
        form = LoginForm()
    return render(request, "login.html", {'form': form})


def home_web(request):
    return render(request, "home.html")

def dashboard_web(request):
    return render(request, "dashboard.html")

def cites_web(request):
    return render(request, "cites.html")

def profile_web(request):
    return render(request, "register.html")

# Demas vistas...
