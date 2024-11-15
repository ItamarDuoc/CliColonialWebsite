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
import time
import threading
import random
from django.db.models import DateField
from django.db.models.functions import Cast


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
        request.session['2fa_code'] = code_2FA
        request.session['numero_celular'] = numero_celular
        for _ in range (10): # Para ver el codigo en la consola sin usar la API por ahora
            print(code_2FA)
        """try:
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
            return JsonResponse({'success': False, 'error': str(e)})"""

    return JsonResponse({'success': False, 'error': 'Método inválido'})

def get_citas_disponibles(request, medico_id, fecha):
    try:
        fecha_obj = datetime.strptime(fecha, '%Y-%m-%d').date()

        medico = Medico.objects.get(id_medico=medico_id)

        horas_todas = [f"{str(h).zfill(2)}:00" for h in range(7, 21)]
        horas_todas += [f"{str(h).zfill(2)}:30" for h in range(7, 20)]

        citas_agendadas = Cita.objects.filter(
            estado='O',
        ).annotate(fecha_cita=Cast('hora_cita', DateField())).filter(fecha_cita=fecha_obj).values_list('hora_cita', flat=True)

        horas_ocupadas = [cita.strftime('%H:%M') for cita in citas_agendadas]

        horas_disponibles = [hora for hora in horas_todas if hora not in horas_ocupadas]

        citas_disponibles = [
            {'id': f"{medico.id_medico}-{fecha}-{hora}", 'descripcion': f"{hora} - {medico.nombre_medico} - {medico.especialidad.nombre_especialidad}"}
            for hora in horas_disponibles
        ]

        return JsonResponse({'citas_disponibles': citas_disponibles})
    
    except Medico.DoesNotExist:
        return JsonResponse({'error': 'Médico no encontrado'}, status=404)
    except Exception as e:
        print(e)  # Esto mostrará el error en la consola del servidor
        return JsonResponse({'error': 'Error interno del servidor'}, status=500)

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

def agendar_hora(usuario, medico, fecha, hora):
    # Logica para agendar una cita en un bloque de tiempo
    try:
        cita = Cita.objects.get(hora_cita=hora, medico=medico, estado="D")  # Buscar cita disponible
        cita.usuario = usuario
        cita.estado = "O"  # Marcar como ocupada
        cita.save()
        return True
    except Cita.DoesNotExist:
        return False

def agendar_consulta_web(request):
    # Usar agendar_hora() para agendar una hora disponible
    medicos = Medico.objects.all()
    print(medicos)
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
        if tiene_suscripcion:
            medico_id = request.POST.get('medico')
            fecha = request.POST.get('fecha')
            hora = request.POST.get('hora')

            hora_cita = timezone.make_aware(datetime.combine(datetime.strptime(fecha, '%Y-%m-%d'), datetime.strptime(hora, '%H:%M').time()))

            medico = Medico.objects.get(id_medico=medico_id)

            if agendar_hora(usuario, medico, fecha, hora_cita):
                messages.success(request, 'Cita agendada con éxito.')
            else:
                messages.error(request, 'No se pudo agendar la cita, intenta con otra hora.')
        else:
            cita_disponible = Cita.objects.filter(estado='D').first()
            if cita_disponible:
                cita_disponible.usuario = usuario
                cita_disponible.estado = 'O'
                cita_disponible.save()
                messages.success(request, f'Cita agendada automáticamente para el {cita_disponible.hora_cita}.')
            else:
                messages.error(request, 'No hay citas disponibles.')

    return render(request, 'agendar_consulta.html', {
        'tiene_suscripcion': tiene_suscripcion,
        'medicos': medicos,
    })

def agendar_examen_web(request):
    return render(request, "agendar_examen.html")

def agendar_seguimiento_web(request):
    return render(request, "agendar_seguimiento.html")

def cites_web(request):
    return render(request, "cites.html")

def profile_web(request):
    return render(request, "profile.html")


# Solucion temeraria para generar bloques de citas para 3 meses cada 1 mes XD
generated_in_day = False

def Generar_Bloques():
    global generated_in_day
    fecha_actual = timezone.now().date()
    primer_dia = fecha_actual.replace(day=1)

    if generated_in_day or (fecha_actual != primer_dia):
        return

    fecha_fin = fecha_actual + timedelta(days=90)

    while fecha_actual <= fecha_fin:
        hora_inicio = timezone.make_aware(datetime.combine(fecha_actual, datetime.min.time()).replace(hour=8, minute=0, second=0), timezone.get_current_timezone())
        hora_fin = timezone.make_aware(datetime.combine(fecha_actual, datetime.min.time()).replace(hour=19, minute=0, second=0), timezone.get_current_timezone())

        while hora_inicio <= hora_fin:
            cita_existente = Cita.objects.filter(hora_cita=hora_inicio).exists()
            if not cita_existente:
                Cita.objects.create(
                    medico=None,
                    usuario=None,
                    tipo_cita="Consulta",
                    hora_cita=hora_inicio,
                    estado="D"
                )
            
            hora_inicio += timedelta(minutes=30)

        fecha_actual += timedelta(days=1)

    generated_in_day = True


def BucleCreador():
    while True:
        try:
            Generar_Bloques()
        except Exception as e:
            time.sleep(10)
            print(f"Error: {e}")
        time.sleep(86400/4) # 4 veces al dia

HiloCreador = threading.Thread(target=BucleCreador)
HiloCreador.start()