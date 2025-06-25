from django.conf import settings
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Usuario
from functools import wraps
from django.shortcuts import redirect
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.http import JsonResponse
import requests
from django.conf import settings
import os
import random


def login_requerido(vista_func):
    @wraps(vista_func)
    def wrapper(request, *args, **kwargs):
        if not request.session.get('usuario_id'):
            return redirect('login')
        return vista_func(request, *args, **kwargs)
    return wrapper

def admin_requerido(vista_func):
    @wraps(vista_func)
    def wrapper(request, *args, **kwargs):
        usuario_id = request.session.get('usuario_id')
        if not usuario_id:
            return redirect('login')
        usuario = Usuario.objects.get(id=usuario_id)
        if usuario.rol != 1:
            messages.error(request, "No tienes permisos para acceder a esta página.")
            return redirect('index')
        return vista_func(request, *args, **kwargs)
    return wrapper

@login_requerido
def index(request):
    usuario = Usuario.objects.get(id=request.session['usuario_id'])
    return render(request, 'index.html', {'usuario': usuario})

def logout(request):
    request.session.flush()
    return redirect('login')

def registro(request):
    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        correo = request.POST.get('correo')
        contraseña = request.POST.get('contraseña')
        confirmar_contraseña = request.POST.get('confirmar_contraseña')
        acepta_terminos = request.POST.get('acepta_terminos') == 'on'

        if not acepta_terminos:
            messages.error(request, "Debes aceptar los términos y condiciones.")
        elif contraseña != confirmar_contraseña:
            messages.error(request, "Las contraseñas no coinciden.")
        elif Usuario.objects.filter(correo=correo).exists():
            messages.error(request, "El correo ya está registrado.")
        else:
            Usuario.objects.create(
                nombre=nombre,
                correo=correo,
                contraseña=contraseña,
                acepta_terminos=acepta_terminos
            )
            messages.success(request, "Usuario registrado correctamente.")
            return redirect('login')
    return render(request, 'registro.html')

def login(request):
    if request.method == 'POST':
        correo = request.POST.get('correo')
        contraseña = request.POST.get('contraseña')
        try:
            usuario = Usuario.objects.get(correo=correo, contraseña=contraseña)
            request.session['usuario_id'] = usuario.id
            messages.success(request, f"Bienvenido, {usuario.nombre}!")
            return redirect('index')  # Asegúrate que 'index' es el nombre de tu url de inicio
        except Usuario.DoesNotExist:
            messages.error(request, "Correo o contraseña incorrectos.")
    return render(request, 'login.html')

@login_requerido
@admin_requerido
def dashboard(request):
    usuario = Usuario.objects.get(id=request.session['usuario_id'])
    usuarios = Usuario.objects.all()
    admins = usuarios.filter(rol=1)
    usuarios_normales = usuarios.filter(rol=0)
    return render(request, 'usuarios_dashboard.html', {
        'usuario': usuario,
        'usuarios': usuarios,
        'admins': admins,
        'usuarios_normales': usuarios_normales,
    })


@login_requerido
@admin_requerido
def registrar_usuario(request):
    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        correo = request.POST.get('correo')
        contraseña = request.POST.get('contraseña')
        rol = int(request.POST.get('rol', 0))
        if Usuario.objects.filter(correo=correo).exists():
            messages.error(request, "El correo ya está registrado.")
        else:
            Usuario.objects.create(
                nombre=nombre,
                correo=correo,
                contraseña=contraseña,
                rol=rol
            )
            messages.success(request, "Usuario registrado correctamente.")
            return redirect('dashboard')
    return render(request, 'registrar_usuario.html')

# Vistas de Administradores

# def es_admin(user):
#     return user.is_superuser

# @user_passes_test(es_admin)
# def dashboard_usuarios(request):
#     usuarios = User.objects.all()
#     return render(request, 'usuarios_dashboard.html', {'usuarios': usuarios})

# @user_passes_test(es_admin)
# def eliminar_usuario(request, user_id):
#     usuario = get_object_or_404(User, id=user_id)
#     usuario.delete()
#     return redirect('dashboard_usuarios')

# @user_passes_test(es_admin)
# def crear_usuario(request):
#     # Aquí iría un formulario personalizado
#     return render(request, 'crear_usuario.html')

# @user_passes_test(es_admin)
# def editar_usuario(request, user_id):
#     # Aquí iría la lógica de edición
#     return render(request, 'editar_usuario.html')


# views.py
from dotenv import load_dotenv


from django.shortcuts import render


load_dotenv()

PEXELS_API_KEY = os.getenv("PEXELS_API_KEY")

def wallpapers(request):
    query = request.GET.get('search', '')
    headers = {'Authorization': PEXELS_API_KEY}
    if query:
        url = f'https://api.pexels.com/v1/search?query={query}&per_page=104'
    else:
        url = 'https://api.pexels.com/v1/curated?per_page=104'
    response = requests.get(url, headers=headers)
    data = response.json() if response.status_code == 200 else {}
    wallpapers = data.get('photos', [])

    # Barajar wallpapers para orden aleatorio en cada recarga
    random.shuffle(wallpapers)

    usuario = None
    usuario_id = request.session.get('usuario_id')
    if usuario_id:
        try:
            usuario = Usuario.objects.get(id=usuario_id)
        except Usuario.DoesNotExist:
            usuario = None

    return render(request, 'wallpaper.html', {
        'wallpapers': wallpapers,
        'query': query,
        'usuario': usuario,  # <-- Agrega esto
    })


from django.views.decorators.http import require_POST





# wallpapers favoritos en vista perfil 
@login_requerido
def perfil(request):
    usuario = Usuario.objects.get(id=request.session['usuario_id'])
    favoritos_ids = usuario.wallpapers_favoritos or []
    wallpapers_favoritos = []

    # Si usas Pexels o una API externa
    PEXELS_API_KEY = os.getenv("PEXELS_API_KEY")
    headers = {'Authorization': PEXELS_API_KEY}

    for wid in favoritos_ids:
        # Suponiendo que wid es el ID de la foto en Pexels
        url = f'https://api.pexels.com/v1/photos/{wid}'
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            wallpapers_favoritos.append(response.json())

    return render(request, 'perfil.html', {
        'usuario': usuario,
        'wallpapers_favoritos': wallpapers_favoritos,
    })


@login_requerido
@require_POST
def toggle_wallpaper_favorito(request, wallpaper_id):
    usuario = Usuario.objects.get(id=request.session['usuario_id'])
    favoritos = usuario.wallpapers_favoritos or []
    wallpaper_id = int(wallpaper_id)
    if wallpaper_id in favoritos:
        favoritos.remove(wallpaper_id)
    else:
        favoritos.append(wallpaper_id)
    usuario.wallpapers_favoritos = favoritos
    usuario.save()
    return redirect('perfil')



import os
import random
import requests
from django.shortcuts import render
from .models import Usuario
def index(request):
    usuario_id = request.session.get('usuario_id')
    if not usuario_id:
        return redirect('login')  # Redirige al login si no hay sesión

    PEXELS_API_KEY = os.getenv("PEXELS_API_KEY")
    headers = {'Authorization': PEXELS_API_KEY}

    temas = {
        "naturaleza": "nature",
        "tecnologia": "technology",
        "arte": "art"
    }
    imagenes = {}

    for key, query in temas.items():
        url = f'https://api.pexels.com/v1/search?query={query}&per_page=30'
        response = requests.get(url, headers=headers)
        data = response.json() if response.status_code == 200 else {}
        fotos = data.get('photos', [])
        if fotos:
            imagenes[key] = random.choice(fotos)['src']['large']
        else:
            imagenes[key] = ""  # O una imagen por defecto

    usuario = Usuario.objects.get(id=usuario_id)

    context = {
        "usuario": usuario,
        "naturaleza_img": imagenes["naturaleza"],
        "tecnologia_img": imagenes["tecnologia"],
        "arte_img": imagenes["arte"],
    }
    return render(request, "index.html", context)