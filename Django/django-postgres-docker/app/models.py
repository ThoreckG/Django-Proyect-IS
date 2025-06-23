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
    


class Equipo(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='equipos')
    nombre = models.CharField(max_length=100)
    # Lista de nombres o IDs de Pokémon (máximo 6)
    pokemones = models.JSONField(default=list, blank=True)

    def save(self, *args, **kwargs):
        if len(self.pokemones) > 6:
            raise ValueError("Un equipo no puede tener más de 6 Pokémon.")
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.nombre} ({self.usuario.nombre})"
    


