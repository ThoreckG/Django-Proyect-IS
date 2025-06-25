from django.db import models

class Usuario(models.Model):
    rol = models.IntegerField(default=0)  # 0 = usuario, 1 = admin
    nombre = models.CharField(max_length=100)
    correo = models.EmailField(unique=True)
    contraseña = models.CharField(max_length=128)
    acepta_terminos = models.BooleanField(default=False)
 
    wallpapers_favoritos = models.JSONField(default=list, blank=True)  # Wallpapers favoritos
    def __str__(self):
        return self.nombre
    



