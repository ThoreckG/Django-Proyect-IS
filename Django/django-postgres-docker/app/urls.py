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
    path('wallpapers/', views.wallpapers, name='wallpapers'),
    path('toggle-wallpaper-favorito/<int:wallpaper_id>/', views.toggle_wallpaper_favorito, name='toggle_wallpaper_favorito'),
    path('eliminar-usuario/<int:usuario_id>/', views.eliminar_usuario, name='eliminar_usuario'),

    
# ...existing code...
    # Administradores
    # path('admin/dashboard/', views.dashboard_usuarios, name='dashboard_usuarios'),
    # path('admin/crear/', views.crear_usuario, name='crear_usuario'),
    # path('admin/editar/<int:user_id>/', views.editar_usuario, name='editar_usuario'),
    # path('admin/eliminar/<int:user_id>/', views.eliminar_usuario, name='eliminar_usuario'),
]