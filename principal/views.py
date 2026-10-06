from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.db.models import Q
from .models import Expediente, PostForo, Comentario
from .forms import ExpedienteForm, RegistroForm, PostForoForm, ComentarioForm

# ----------------- EXPEDIENTES (OFICIALES) -----------------
def lista_expedientes(request):
    region_filtro = request.GET.get('region', 'TODOS')
    busqueda = request.GET.get('q', '')

    expedientes = Expediente.objects.all().order_by('-id')

    if region_filtro != 'TODOS' and region_filtro:
        expedientes = expedientes.filter(ubicacion=region_filtro)

    if busqueda:
        expedientes = expedientes.filter(
            Q(titulo__icontains=busqueda) | Q(descripcion__icontains=busqueda)
        )

    form = ExpedienteForm()
    if request.method == 'POST' and request.user.is_authenticated:
        form = ExpedienteForm(request.POST)
        if form.is_valid():
            nuevo = form.save(commit=False)
            nuevo.autor = request.user
            nuevo.save()
            return redirect('inicio')

    return render(request, 'index.html', {
        'expedientes': expedientes,
        'form': form,
        'filtro_actual': region_filtro,
        'busqueda': busqueda,
    })

# SOLO EL ADMIN PUEDE ELIMINAR EXPEDIENTES
@staff_member_required
def eliminar_expediente(request, id):
    expediente = get_object_or_404(Expediente, id=id)
    expediente.delete()
    return redirect('inicio')

# ----------------- FORO / BLOG (TIPO REDDIT) -----------------
def vista_foro(request):
    categoria_filtro = request.GET.get('cat', 'TODAS')
    posts = PostForo.objects.all().order_by('-creado_en')

    if categoria_filtro != 'TODAS' and categoria_filtro:
        posts = posts.filter(categoria=categoria_filtro)

    form = PostForoForm()
    comentario_form = ComentarioForm()

    if request.method == 'POST' and request.user.is_authenticated:
        form = PostForoForm(request.POST)
        if form.is_valid():
            nuevo_post = form.save(commit=False)
            nuevo_post.autor = request.user
            nuevo_post.save()
            return redirect('foro')

    return render(request, 'foro.html', {
        'posts': posts,
        'form': form,
        'comentario_form': comentario_form,
        'categoria_actual': categoria_filtro
    })

# Comentar en un post
@login_required
def agregar_comentario(request, post_id):
    post = get_object_or_404(PostForo, id=post_id)
    if request.method == 'POST':
        form = ComentarioForm(request.POST)
        if form.is_valid():
            comentario = form.save(commit=False)
            comentario.post = post
            comentario.autor = request.user
            comentario.save()
    return redirect('foro')

# Dar o quitar Like
@login_required
def dar_like(request, post_id):
    post = get_object_or_404(PostForo, id=post_id)
    if request.user in post.likes.all():
        post.likes.remove(request.user)
    else:
        post.likes.add(request.user)
    return redirect('foro')

# Editar propio post
@login_required
def editar_post(request, post_id):
    post = get_object_or_404(PostForo, id=post_id)
    if post.autor != request.user and not request.user.is_staff:
        return redirect('foro')

    if request.method == 'POST':
        form = PostForoForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            return redirect('foro')
    else:
        form = PostForoForm(instance=post)
    return render(request, 'editar_post.html', {'form': form, 'post': post})

# Eliminar post del foro (El dueño o el Admin)
@login_required
def eliminar_post(request, post_id):
    post = get_object_or_404(PostForo, id=post_id)
    if post.autor == request.user or request.user.is_staff:
        post.delete()
    return redirect('foro')

# ----------------- LOGIN / REGISTRO / LOGOUT -----------------
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('inicio')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

def registro_view(request):
    if request.method == 'POST':
        form = RegistroForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('inicio')
    else:
        form = RegistroForm()
    return render(request, 'registro.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('inicio')