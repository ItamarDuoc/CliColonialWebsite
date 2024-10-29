from django.shortcuts import render, redirect
from .models import *
from .forms import RegistroForm, LoginForm
from django.contrib.auth import login, authenticate
from django.contrib import messages
import secrets
from twilio.rest import Client
from django.http import JsonResponse
from .utils import cifrar_dato, descifrar_dato
from django.utils import timezone
from datetime import timedelta, datetime
import random


# UTILES
def verificar_suscripcion_activa(usuario):
    try:
        suscripcion = Suscripcion.objects.get(usuario=usuario)
        if suscripcion.estado == 'Y' and suscripcion.fecha_termino >= timezone.now().date():
            return True
    except Suscripcion.DoesNotExist:
        return False
    return False

def gen_2fa_code():
    return ''.join(secrets.choice('0123456789') for _ in range(6))

def send_2fa_code(request):
    if request.method == 'POST':
        numero_celular = request.POST.get('numero_celular')
        if not numero_celular:
            return JsonResponse({'success': False, 'error': 'Número de celular no proporcionado'})
        code_2FA = gen_2fa_code()
        #request.session['2fa_code'] = code_2FA
        #request.session['numero_celular'] = numero_celular
        #for _ in range (10): # Para ver el codigo en la consola sin usar la API por ahora
        #    print(code_2FA)
        try:
            account_sid = ''
            auth_token = ''
            twilio_number = '+'
            client = Client(account_sid, auth_token)

            message = client.messages.create(
                body=f"Tu código de verificación es: {code_2FA}",
                from_=twilio_number,
                to=f'+{numero_celular}'
            )

            request.session['2fa_code'] = code_2FA
            request.session['numero_celular'] = numero_celular

            return JsonResponse({'success': True})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})

    return JsonResponse({'success': False, 'error': 'Método inválido'})

# VISTAS
def registro_web(request):
    if request.method == 'POST':
        nombre_usuario = request.POST.get('nombre_usuario')
        numero_celular = request.POST.get('numero_celular')
        run = request.POST.get('run')
        numero_documento = request.POST.get('numero_documento')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        codigo_2fa = request.POST.get('codigo_2fa')

        if password == confirm_password:
            encript_password = cifrar_dato(password)
            encript_numero_doc = cifrar_dato(numero_documento)
            encript_numero_celular = cifrar_dato(numero_celular)

            codigo_enviado = request.session.get('2fa_code')

            if codigo_enviado == codigo_2fa:
                usuario = Usuario(
                    nombre_usuario=nombre_usuario,
                    numero_celular=encript_numero_celular,
                    run=run,
                    numero_documento=encript_numero_doc,
                    password=encript_password
                )
                usuario.save()

                suscripcion = Suscripcion(
                    usuario=usuario,
                    fecha_inicio=timezone.now(),
                    fecha_termino=timezone.now() + timedelta(days=30),
                    estado='N', # Valor por defecto -> Sin suscripcion
                    tarjeta=None 
                )
                suscripcion.save()
                request.session['id_usuario'] = usuario.id_usuario
                messages.success(request, '¡Registro exitoso!')
                return redirect('home')
            else:
                messages.error(request, 'Código 2FA incorrecto')
        else:
            messages.error(request, 'Las contraseñas no coinciden')

    return render(request, 'register.html') 

def login_web(request):
    if request.method == 'POST':
        run = request.POST.get('run')
        numero_documento = request.POST.get('numero_documento')
        numero_celular = request.POST.get('numero_celular')
        password = request.POST.get('password')
        codigo_2fa = request.POST.get('codigo_2fa')

        try:
            usuario = Usuario.objects.get(run=run)
            descifrado_numero_doc = descifrar_dato(usuario.numero_documento)
            descifrado_numero_celular = descifrar_dato(usuario.numero_celular)

            if descifrado_numero_doc == numero_documento and descifrado_numero_celular == numero_celular:
                if descifrar_dato(usuario.password) == password:
                    codigo_enviado = request.session.get('2fa_code')
                    if codigo_enviado == codigo_2fa:
                        request.session['id_usuario'] = usuario.id_usuario
                        messages.success(request, f'¡Bienvenido {usuario.nombre_usuario}!')
                        return redirect('home')
                    else:
                        messages.error(request, 'Código 2FA incorrecto')
                else:
                    messages.error(request, 'Contraseña incorrecta')
            else:
                messages.error(request, 'Número de documento o celular incorrecto')
        except Usuario.DoesNotExist:
            messages.error(request, 'Usuario no encontrado')

    return render(request, 'login.html')

def home_web(request):
    return render(request, "home.html")

def dashboard_web(request):
    return render(request, "dashboard.html")

def agendar_consulta_web(request):
    if not request.session.get('id_usuario'):
        return redirect('/login')

    usuario_id = request.session['id_usuario']
    usuario = Usuario.objects.get(id_usuario=usuario_id)

    try:
        suscripcion = Suscripcion.objects.get(usuario=usuario)
    except Suscripcion.DoesNotExist:
        suscripcion = None

    tiene_suscripcion = suscripcion and suscripcion.estado == 'Y' and suscripcion.fecha_termino > timezone.now().date()

    if request.method == 'POST':
        hora_actual_mas_una = timezone.now() + timedelta(hours=1)
        fecha_cita = hora_actual_mas_una.strftime("%Y-%m-%d %H:%M:%S")
        if tiene_suscripcion:
            medico_id = request.POST.get('medico_id')
            medico = Medico.objects.get(id_medico=medico_id)
        else:
            medicos_disponibles = Medico.objects.all()
            if medicos_disponibles.exists():
                medico = random.choice(medicos_disponibles)
            else:
                messages.error(request, 'No hay médicos disponibles en este momento.')
                return redirect('/agendar-consulta')

        Cita.objects.create(
            medico=medico,
            usuario=usuario,
            tipo_cita="Consulta",
            hora_cita=fecha_cita,
            estado="O",
        )
        return redirect('/confirmacion')

    context = {
        'tiene_suscripcion': tiene_suscripcion,
    }

    return render(request, 'agendar_consulta.html', context)

def agendar_examen_web(request):
    return render(request, "agendar_examen.html")

def agendar_seguimiento_web(request):
    return render(request, "agendar_seguimiento.html")

def cites_web(request):
    return render(request, "cites.html")

def profile_web(request):
    return render(request, "profile.html")
