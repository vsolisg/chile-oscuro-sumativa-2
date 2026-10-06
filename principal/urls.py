from django.urls import path
from . import views

urlpatterns = [
    # Expedientes
    path('', views.lista_expedientes, name='inicio'),
    path('expediente/eliminar/<int:id>/', views.eliminar_expediente, name='eliminar_expediente'),
    
    # Foro
    path('foro/', views.vista_foro, name='foro'),
    path('foro/like/<int:post_id>/', views.dar_like, name='dar_like'),
    path('foro/comentar/<int:post_id>/', views.agregar_comentario, name='agregar_comentario'),
    path('foro/editar/<int:post_id>/', views.editar_post, name='editar_post'),
    path('foro/eliminar/<int:post_id>/', views.eliminar_post, name='eliminar_post'),

    # Autenticación
    path('login/', views.login_view, name='login'),
    path('registro/', views.registro_view, name='registro'),
    path('logout/', views.logout_view, name='logout'),
]