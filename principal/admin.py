from django.contrib import admin
from .models import Expediente, PostForo, Comentario

# Registramos los modelos para que aparezcan en el panel de administración
admin.site.register(Expediente)
admin.site.register(PostForo)
admin.site.register(Comentario)