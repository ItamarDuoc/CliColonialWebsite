from django.shortcuts import render, redirect
from .models import Usuario
from .forms import RegistroForm, LoginForm
from django.contrib.auth import login, authenticate
from django.contrib import messages  # Para mostrar mensajes de error

import bcrypt, secrets, os
from twilio.rest import Client # Libreria para SMS
from dotenv import load_dotenv

def gen_2fa_code(usuario):
    return ''.join(secrets.choice('0123456789') for _ in range(6))

def send_2fa_code(code, numero_telefono):
    try:
        account_sid = os.getenv('')
        auth_token = os.getenv('')
        twilio_number = os.getenv('+')
    
        client = Client(account_sid, auth_token)
    
        message = client.messages.create(
            body = f"Tu codigo de verificacion para Clinica Colonial es: {code}",
            from_ = twilio_number,
            to = numero_telefono, 
        )

        print(f"SMS enviado: {message.sid}")
        print(message.body)
    except Exception as e:
        raise ValueError(str(e) + "Error al enviar SMS")

def registro_web(request):
    # Verificar si el usuario ya ha iniciado sesion
    # Si no ha iniciado sesion, esperar un metodo Post del formulario para registrar la cuenta
    # Generar un numero al azar de 6 digitos del 0 al 999999, este se utilizara para el 2FA
    # El registro debe registrar los datos: nombre_usuario, numero_celular, run, numero_documento. El ID del usuario se genera automaticamente y la foto de perfil quedará vacia.
    # Se debe validar que los datos cumplan con un patron valido y que el 2FA sea correcto.
    # Utilizar la libreria bcrypt para encriptar los datos sensibles.
    # Validar los datos, si el registro es exitoso, redireccionar a "/home"
    return "Realizar logica: Pendiente"


def login_web(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            run = form.cleaned_data['run']
            password = form.cleaned_data['password']
            try:
                usuario = Usuario.objects.get(run=run)
                if bcrypt.checkpw(password.encode('utf-8'), usuario.password.encode('utf-8')):  
                    return redirect('home')
                else:
                    messages.error(request, 'Contraseña incorrecta.')
            except Usuario.DoesNotExist:
                messages.error(request, 'Usuario no encontrado.')
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})


def home_web(request):
    return render(request, "home.html")

def dashboard_web(request):
    return render(request, "dashboard.html")

def cites_web(request):
    return render(request, "cites.html")

def profile_web(request):
    return render(request, "register.html")

# Demas vistas...
