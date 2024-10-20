from cryptography.fernet import Fernet
from django.conf import settings

# Función para cifrar datos
def cifrar_dato(dato):
    fernet = Fernet(settings.SECRET_KEY_CRYPT.encode())  # Crear el objeto Fernet con la clave
    return fernet.encrypt(dato.encode()).decode()  # Cifrar y devolver como string legible

# Función para descifrar datos
def descifrar_dato(dato_cifrado):
    fernet = Fernet(settings.SECRET_KEY_CRYPT.encode())  # Crear el objeto Fernet con la clave
    return fernet.decrypt(dato_cifrado.encode()).decode()  # Descifrar y devolver el string original
