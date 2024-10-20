from django.db import models

class Usuario(models.Model):
    id_usuario = models.AutoField(primary_key=True)
    nombre_usuario = models.CharField(max_length=100)
    numero_celular = models.IntegerField()
    run = models.CharField(max_length=12, unique=True)
    numero_documento = models.IntegerField(unique=True)
    foto_perfil = models.BinaryField(null=True, blank=True)

    def __str__(self):
        return self.nombre_usuario

class Tarjeta(models.Model):
    numero_tarjeta = models.IntegerField(primary_key=True)
    CVV = models.IntegerField()
    fecha_caducidad = models.DateField()
    usuario = models.OneToOneField(Usuario, on_delete=models.CASCADE)

class Suscripcion(models.Model):
    id_suscripcion = models.AutoField(primary_key=True)
    fecha_inicio = models.DateField()
    fecha_termino = models.DateField()
    estado = models.CharField(max_length=1) # Activa ('A'), Inactiva ('I') 
    usuario = models.OneToOneField(Usuario, on_delete=models.CASCADE)
    tarjeta = models.ForeignKey(Tarjeta, on_delete=models.CASCADE)

class Medico(models.Model):
    id_medico = models.AutoField(primary_key=True)
    nombre_medico = models.CharField(max_length=100)
    especialidad = models.ForeignKey('Especialidad', on_delete=models.CASCADE)

    def __str__(self):
        return self.nombre_medico

class Especialidad(models.Model):
    id_especialidad = models.AutoField(primary_key=True)
    nombre_especialidad = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre_especialidad

class Administrador(models.Model):
    id_administrador = models.AutoField(primary_key=True)
    nombre_administrador = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre_administrador

class Cita(models.Model):
    id_cita = models.AutoField(primary_key=True)
    medico = models.ForeignKey(Medico, on_delete=models.CASCADE)
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    tipo_cita = models.CharField(max_length=100)  # Ejemplo: "Consulta", "Revisión"
    hora_cita = models.DateTimeField()
    estado = models.CharField(max_length=1)  # Pendiente ('P'), Completada ('C'), Cancelada ('X')
    administrador = models.ForeignKey(Administrador, on_delete=models.SET_NULL, null=True, blank=True)