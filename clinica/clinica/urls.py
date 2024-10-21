from django.contrib import admin
from django.urls import path
from django.views.generic import RedirectView

from citas import views

urlpatterns = [
    path('admin/', admin.site.urls, name="admin"),
    path('register/', views.registro_web, name="register"),
    path('login/',views.login_web, name="login"),
    path('home/',views.home_web, name="home"),
    path('profile/',views.profile_web, name="profile"),

    path('dashboard/',views.dashboard_web, name="dashboard"),
    path('agendar-consulta/', views.agendar_consulta_web, name="agendar_consulta"),
    path('agendar-examen/', views.agendar_examen_web, name="agendar_examen"),
    path('agendar-seguimiento/', views.agendar_seguimiento_web, name="agendar_seguimiento"),

    path('cites/',views.cites_web, name="cites"),
    path('', RedirectView.as_view(url='/home/', permanent=True), name="default"), # -> Para evitar la pagina de error
    path('send_2fa_code/', views.send_2fa_code, name='send_2fa_code'),  # URL para enviar el codigo 2FA
]
