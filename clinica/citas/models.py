from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models

class UsuarioManager(BaseUserManager):
    def create_user(self, nombre_usuario, run, numero_documento, numero_celular, password=None):
        if not run:
            raise ValueError("El usuario debe tener un RUN válido")
        user = self.model(
            nombre_usuario=nombre_usuario,
            run=run,
            numero_documento=numero_documento,
            numero_celular=numero_celular
        )
        user.set_password(password)  # Esto asegurará que la contraseña se almacene de forma segura
        user.save(using=self._db)
        return user

    def create_superuser(self, nombre_usuario, run, numero_documento, numero_celular, password):
        user = self.create_user(
            nombre_usuario=nombre_usuario,
            run=run,
            numero_documento=numero_documento,
            numero_celular=numero_celular,
            password=password
        )
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

class Usuario(AbstractBaseUser, PermissionsMixin):
    id_usuario = models.AutoField(primary_key=True)
    nombre_usuario = models.CharField(max_length=100, unique=True)
    numero_celular = models.IntegerField()
    run = models.CharField(max_length=12, unique=True)
    numero_documento = models.IntegerField(unique=True)
    # Eliminar la foto de perfil si no es necesaria
    # foto_perfil = models.BinaryField(null=True, blank=True)

    # Campos adicionales para soporte de autenticación y permisos
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)  # Para acceso a /admin
    is_superuser = models.BooleanField(default=False)  # Superusuario con todos los permisos

    groups = models.ManyToManyField(
        'auth.Group',
        related_name='usuario_set',
        blank=True,
        help_text='Grupos a los que pertenece el usuario.'
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='usuario_permissions_set',
        blank=True,
        help_text='Permisos específicos para el usuario.'
    )

    objects = UsuarioManager()

    USERNAME_FIELD = 'run'
    REQUIRED_FIELDS = ['nombre_usuario', 'numero_documento', 'numero_celular']

    def __str__(self):
        return self.nombre_usuario

# Resto de tus modelos permanece igual
