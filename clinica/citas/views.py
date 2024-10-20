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
    code_2FA = gen_2fa_code()
    # Verificar si el usuario ya ha iniciado sesion
    # Si no ha iniciado sesion, esperar un metodo Post del formulario para registrar la cuenta
    # El registro debe registrar los datos: nombre_usuario, numero_celular, run, numero_documento. El ID del usuario se genera automaticamente y la foto de perfil quedará vacia.
    # Se debe validar que los datos cumplan con un patron valido y que el 2FA sea correcto.
    # Utilizar la libreria bcrypt para encriptar los datos sensibles.
    # Validar los datos, si el registro es exitoso, redireccionar a "/home"
    return "Realizar logica: Pendiente"


def login_web(request):
    code_2FA = gen_2fa_code()
    # Verificar si el usuario ya ha iniciado sesion
    # Si no ha iniciado sesion, esperar un metodo Post del formulario para loguear la cuenta
    # El registro debe registrar los datos: nombre_usuario, numero_celular, run, numero_documento. El ID del usuario se genera automaticamente y la foto de perfil quedará vacia.
    # Se debe validar que los datos cumplan con un patron valido, que sean correctos y que el 2FA sea correcto.
    return "Realizar logica: Pendiente"


def home_web(request):
    return render(request, "home.html")

def dashboard_web(request):
    return render(request, "dashboard.html")

def cites_web(request):
    return render(request, "cites.html")

def profile_web(request):
    return render(request, "register.html")

# Demas vistas...
