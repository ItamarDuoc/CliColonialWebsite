# Generated by Django 5.0.6 on 2024-10-21 12:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('citas', '0003_alter_usuario_numero_celular_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='suscripcion',
            name='estado',
            field=models.CharField(default='N', max_length=1),
        ),
    ]
