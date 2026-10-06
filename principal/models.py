from django.db import models
from django.contrib.auth.models import User

class Expediente(models.Model):
    TIPO_CHOICES = [
        ('CRIMINAL', 'Criminal'),
        ('LEYENDA', 'Leyenda'),
        ('MITO', 'Mito'),
    ]
    ZONA_CHOICES = [
        ('NORTE', 'Norte'),
        ('CENTRO', 'Centro'),
        ('SUR', 'Sur'),
        ('AUSTRAL', 'Austral'),
    ]
    titulo = models.CharField(max_length=200)
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES)
    ubicacion = models.CharField(max_length=100)
    zona = models.CharField(max_length=20, choices=ZONA_CHOICES, blank=True)
    imagen = models.CharField(max_length=255, blank=True, null=True)
    descripcion = models.TextField()
    autor = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    creado_en = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        zonas_map = {
            "NORTE": ["ARICA Y PARINACOTA", "TARAPACÁ", "ANTOFAGASTA", "ATACAMA", "COQUIMBO"],
            "CENTRO": ["VALPARAÍSO", "METROPOLITANA", "O'HIGGINS", "MAULE", "ÑUBLE", "BÍOBÍO"],
            "SUR": ["LA ARAUCANÍA", "LOS RÍOS", "LOS LAGOS"],
            "AUSTRAL": ["AYSÉN", "MAGALLANES Y DE LA ANTÁRTICA CHILENA"]
        }
        for nombre_zona, regiones in zonas_map.items():
            if self.ubicacion in regiones:
                self.zona = nombre_zona
                break
        super().save(*args, **kwargs)

    def __str__(self):
        return self.titulo

# Modelo del Foro (Estilo Reddit / Blog)
class PostForo(models.Model):
    CATEGORIAS = [
        ('PROPIO', 'Relato Propio'),
        ('PARANORMAL', 'Paranormal'),
        ('TEORIA', 'Investigación / Teoría'),
        ('DEBATE', 'Debate General'),
    ]
    autor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    titulo = models.CharField(max_length=200)
    categoria = models.CharField(max_length=20, choices=CATEGORIAS, default='PROPIO')
    contenido = models.TextField()
    creado_en = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(User, related_name='posts_con_like', blank=True)

    def total_likes(self):
        return self.likes.count()

    def __str__(self):
        return f"{self.titulo} - {self.autor.username}"

# Comentarios del Foro
class Comentario(models.Model):
    post = models.ForeignKey(PostForo, on_delete=models.CASCADE, related_name='comentarios')
    autor = models.ForeignKey(User, on_delete=models.CASCADE)
    texto = models.TextField()
    creado_en = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comentario de {self.autor.username} en {self.post.titulo}"