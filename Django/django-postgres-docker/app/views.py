from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Usuario, Equipo
from functools import wraps
from django.shortcuts import redirect
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.http import JsonResponse
import requests

def login_requerido(vista_func):
    @wraps(vista_func)
    def wrapper(request, *args, **kwargs):
        if not request.session.get('usuario_id'):
            return redirect('wallpapers')
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
            return redirect('wallpapers')
        return vista_func(request, *args, **kwargs)
    return wrapper

@login_requerido
def index(request):
    usuario = Usuario.objects.get(id=request.session['usuario_id'])
    return render(request, 'wallpaper.html', {'usuario': usuario})

def logout(request):
    request.session.flush()
    return redirect('wallpapers')

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
def pokemon(request):
    usuario = Usuario.objects.get(id=request.session['usuario_id'])
    offset = int(request.GET.get('offset', 0))
    response = requests.get(f'https://pokeapi.co/api/v2/pokemon?limit=20&offset={offset}')
    pokemon_list = []
    next_offset = prev_offset = None
    if response.status_code == 200:
        data = response.json()
        for poke in data['results']:
            poke_data = requests.get(poke['url']).json()
            pokemon_list.append({
                'name': poke_data['name'],
                'image': poke_data['sprites']['front_default'],
                'types': [t['type']['name'] for t in poke_data['types']],
                'id': poke_data['id'],
            })
        # Manejo de paginación
        if data['next']:
            next_offset = offset + 20
        if data['previous']:
            prev_offset = max(offset - 20, 0)
    return render(request, 'pokemon_dashboard.html', {
        'usuario': usuario,
        'pokemon': pokemon_list,
        'next_offset': next_offset,
        'prev_offset': prev_offset,
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

@login_requerido
def perfil(request):
    usuario = Usuario.objects.get(id=request.session['usuario_id'])
    favoritos_data = []
    for poke_id in usuario.favoritos:
        response = requests.get(f'https://pokeapi.co/api/v2/pokemon/{poke_id}')
        if response.status_code == 200:
            poke = response.json()
            favoritos_data.append({
                'id': poke['id'],
                'name': poke['name'],
                'image': poke['sprites']['front_default'],
                'types': [t['type']['name'] for t in poke['types']],
            })

    equipos_data = []
    for equipo in usuario.equipos.all():
        pokemones = []
        for poke_id in equipo.pokemones:
            response = requests.get(f'https://pokeapi.co/api/v2/pokemon/{poke_id}')
            if response.status_code == 200:
                poke = response.json()
                pokemones.append({
                    'id': poke['id'],
                    'name': poke['name'],
                    'image': poke['sprites']['front_default'],
                    'types': [t['type']['name'] for t in poke['types']],
                })
        equipos_data.append({
            'nombre': equipo.nombre,
            'pokemones': pokemones,
        })

    return render(request, 'perfil.html', {
        'usuario': usuario,
        'favoritos': favoritos_data,
        'equipos': equipos_data,
    })

@login_requerido
def pokemon_detalle(request, poke_id):
    usuario = Usuario.objects.get(id=request.session['usuario_id'])
    response = requests.get(f'https://pokeapi.co/api/v2/pokemon/{poke_id}')
    if response.status_code == 200:
        poke = response.json()
    else:
        poke = None
    return render(request, 'pokemon.html', {'usuario': usuario, 'poke': poke})

@login_requerido
@require_POST
def agregar_a_equipo(request):
    usuario = Usuario.objects.get(id=request.session['usuario_id'])
    poke_id = request.POST.get('poke_id')
    equipo_id = request.POST.get('equipo_id')
    nuevo_equipo = request.POST.get('nuevo_equipo', '').strip()

    # Si el usuario quiere crear un nuevo equipo
    if nuevo_equipo:
        equipo = Equipo.objects.create(usuario=usuario, nombre=nuevo_equipo, pokemones=[poke_id])
        return JsonResponse({'success': True, 'equipo': equipo.nombre})

    # Si seleccionó un equipo existente
    if equipo_id:
        try:
            equipo = Equipo.objects.get(id=equipo_id, usuario=usuario)
            if poke_id in equipo.pokemones:
                return JsonResponse({'success': False, 'error': 'Este Pokémon ya está en el equipo.'})
            if len(equipo.pokemones) >= 6:
                return JsonResponse({'success': False, 'error': 'El equipo ya tiene 6 Pokémon.'})
            equipo.pokemones.append(poke_id)
            equipo.save()
            return JsonResponse({'success': True, 'equipo': equipo.nombre})
        except Equipo.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Equipo no encontrado.'})

    return JsonResponse({'success': False, 'error': 'No se seleccionó equipo.'})

@login_requerido
@require_POST
def cambiar_nombre_equipo(request):
    equipo_id = request.POST.get('equipo_id')
    nuevo_nombre = request.POST.get('nuevo_nombre')
    equipo = Equipo.objects.get(nombre=equipo_id, usuario__id=request.session['usuario_id'])
    equipo.nombre = nuevo_nombre
    equipo.save()
    return JsonResponse({'success': True})

@login_requerido
@require_POST
def eliminar_equipo(request):
    equipo_id = request.POST.get('equipo_id')
    equipo = Equipo.objects.get(nombre=equipo_id, usuario__id=request.session['usuario_id'])
    equipo.delete()
    return JsonResponse({'success': True})

@login_requerido
@require_POST
def toggle_favorito(request):
    usuario = Usuario.objects.get(id=request.session['usuario_id'])
    poke_id = request.POST.get('poke_id')
    if not poke_id:
        return JsonResponse({'success': False, 'error': 'No se proporcionó poke_id.'})

    favoritos = usuario.favoritos or []
    if poke_id in favoritos:
        favoritos.remove(poke_id)
        action = 'removed'
    else:
        favoritos.append(poke_id)
        action = 'added'
    usuario.favoritos = favoritos
    usuario.save()
    return JsonResponse({'success': True, 'action': action})

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
import os


load_dotenv()
PEXELS_API_KEY = os.getenv("PEXELS_API_KEY")





from django.shortcuts import render


load_dotenv()
PEXELS_API_KEY = os.getenv("PEXELS_API_KEY")

def wallpapers(request):
    query = request.GET.get('search', '')
    headers = {'Authorization': PEXELS_API_KEY}
    if query:
        url = f'https://api.pexels.com/v1/search?query={query}&per_page=4'
    else:
        url = 'https://api.pexels.com/v1/curated?per_page=16'
    response = requests.get(url, headers=headers)
    data = response.json() if response.status_code == 200 else {}
    wallpapers = data.get('photos', [])

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



@login_requerido
@require_POST
def toggle_wallpaper_favorito(request):
    usuario = Usuario.objects.get(id=request.session['usuario_id'])
    wallpaper_id = request.POST.get('wallpaper_id')
    if not wallpaper_id:
        return JsonResponse({'success': False, 'error': 'No se proporcionó wallpaper_id.'})

    favoritos = usuario.wallpapers_favoritos or []
    if wallpaper_id in favoritos:
        favoritos.remove(wallpaper_id)
        action = 'removed'
    else:
        favoritos.append(wallpaper_id)
        action = 'added'
    usuario.wallpapers_favoritos = favoritos
    usuario.save()
    return JsonResponse({'success': True, 'action': action})


# wallpapers favoritos en vista perfil 
@login_requerido
def perfil(request):
    usuario = Usuario.objects.get(id=request.session['usuario_id'])
    wallpapers_favoritos = usuario.wallpapers_favoritos or []
    return render(request, 'perfil.html', {
        'usuario': usuario,
        'wallpapers_favoritos': wallpapers_favoritos,
    })