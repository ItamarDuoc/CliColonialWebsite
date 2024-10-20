"""
URL configuration for clinica project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.views.generic import RedirectView

from citas import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('register/', views.registro_web),
    path('login/',views.login_web),
    path('home/',views.home_web),
    path('profile/',views.profile_web),
    path('dashboard/',views.dashboard_web),
    path('', RedirectView.as_view(url='/home/', permanent=True)) # -> Para evitar la pagina de error
]
