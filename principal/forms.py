from django import forms
from django.contrib.auth.models import User
from .models import Expediente, PostForo, Comentario

REGIONES = [
    ('', 'Selecciona Región'),
    ('ARICA Y PARINACOTA', 'ARICA Y PARINACOTA'),
    ('TARAPACÁ', 'TARAPACÁ'),
    ('ANTOFAGASTA', 'ANTOFAGASTA'),
    ('ATACAMA', 'ATACAMA'),
    ('COQUIMBO', 'COQUIMBO'),
    ('VALPARAÍSO', 'VALPARAÍSO'),
    ('METROPOLITANA', 'METROPOLITANA'),
    ("O'HIGGINS", "O'HIGGINS"),
    ('MAULE', 'MAULE'),
    ('ÑUBLE', 'ÑUBLE'),
    ('BÍOBÍO', 'BÍOBÍO'),
    ('LA ARAUCANÍA', 'LA ARAUCANÍA'),
    ('LOS RÍOS', 'LOS RÍOS'),
    ('LOS LAGOS', 'LOS LAGOS'),
    ('AYSÉN', 'AYSÉN'),
    ('MAGALLANES Y DE LA ANTÁRTICA CHILENA', 'MAGALLANES Y DE LA ANTÁRTICA CHILENA'),
]

class ExpedienteForm(forms.ModelForm):
    ubicacion = forms.ChoiceField(choices=REGIONES)
    class Meta:
        model = Expediente
        fields = ['titulo', 'tipo', 'ubicacion', 'descripcion']

# Formulario para registro con contraseña encriptada
class RegistroForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Contraseña'}))
    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"]) # Encriptación nativa PBKDF2/SHA-256
        if commit:
            user.save()
        return user

# Formulario de Publicación en el Foro
class PostForoForm(forms.ModelForm):
    class Meta:
        model = PostForo
        fields = ['titulo', 'categoria', 'contenido']
        widgets = {
            'titulo': forms.TextInput(attrs={'placeholder': 'Título del reporte o relato...'}),
            'contenido': forms.Textarea(attrs={'placeholder': 'Escribe aquí tu experiencia o investigación...'}),
        }

# Formulario de Comentarios
class ComentarioForm(forms.ModelForm):
    class Meta:
        model = Comentario
        fields = ['texto']
        widgets = {
            'texto': forms.TextInput(attrs={'placeholder': 'Escribe un comentario...'}),
        }