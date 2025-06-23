from django.contrib import admin
from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('registro/', views.registro, name='registro'),
    path('login/', views.login, name='login'),
    path('dashboard/', views.dashboard, name='dashboard'),
    
    path('registrar-usuario/', views.registrar_usuario, name='registrar_usuario'),
    path('logout/', views.logout, name='logout'),
    path('perfil/', views.perfil, name='perfil'),
    path('pokemon/<int:poke_id>/', views.pokemon_detalle, name='pokemon_detalle'),
    path('toggle-favorito/', views.toggle_favorito, name='toggle_favorito'),
    path('agregar-a-equipo/', views.agregar_a_equipo, name='agregar_a_equipo'),
    path('cambiar-nombre-equipo/', views.cambiar_nombre_equipo, name='cambiar_nombre_equipo'),
    path('eliminar-equipo/', views.eliminar_equipo, name='eliminar_equipo'),
    
    path('wallpapers/', views.wallpapers, name='wallpapers'),
    
    # Administradores
    # path('admin/dashboard/', views.dashboard_usuarios, name='dashboard_usuarios'),
    # path('admin/crear/', views.crear_usuario, name='crear_usuario'),
    # path('admin/editar/<int:user_id>/', views.editar_usuario, name='editar_usuario'),
    # path('admin/eliminar/<int:user_id>/', views.eliminar_usuario, name='eliminar_usuario'),
]