from django.shortcuts import render
from .models import *
import bcrypt

def registro_web(request):
    return render(request, "register.html")

def login_web(request):
    return render(request, "login.html")

def registrar_usuario(request):
    return

def loguear_usuario(request):
    return

def home_web(request):
    return render(request, "home.html")

def dashboard_web(request):
    return render(request, "dashboard.html")

def profile_web(request):
    return render(request, "register.html")

# Demas vistas...