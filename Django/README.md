# Proyecto Django: Gestión de Usuarios y Libros

Este proyecto es una aplicación web desarrollada con **Django**, **PostgreSQL** y **Docker**, orientada a la gestión de usuarios y libros, con autenticación personalizada y panel de administración.

## Características principales

- **Registro y login de usuarios** personalizados (modelo propio, no el de Django por defecto).
- **Roles de usuario**: usuario normal y administrador.
- **Gestión de libros**: cada usuario puede marcar libros como favoritos.
- **Panel de administración** protegido para administradores.
- **Protección de rutas** mediante sesiones y decoradores personalizados.
- **Panel de administración de Django** habilitado para gestionar usuarios y libros.
- **Interfaz moderna** con Bootstrap y soporte para modo oscuro.
- **Archivos estáticos** (CSS) correctamente configurados y servidos.
- **Despliegue y desarrollo con Docker** y Docker Compose.

## Estructura de carpetas relevante

```
django-postgres-docker/
│
├── app/
│   ├── static/
│   │   └── styles/
│   │       ├── app.css
│   │       └── registro.css
│   ├── templates/
│   │   ├── index.html
│   │   ├── login.html
│   │   ├── registro.html
│   │   ├── usuarios_dashboard.html
│   │   └── libros_dashboard.html
│   ├── models.py
│   ├── views.py
│   ├── forms.py
│   ├── admin.py
│   └── ...
├── docker-compose.yml
├── Dockerfile
└── ...
```

## Tecnologías utilizadas

- **Django** (backend y ORM)
- **PostgreSQL** (base de datos)
- **Docker** y **Docker Compose** (desarrollo y despliegue)
- **Bootstrap** (frontend)
- **HTML/CSS** (plantillas y estilos)

## Cómo ejecutar el proyecto

1. Clona el repositorio.
2. Asegúrate de tener Docker y Docker Compose instalados.
3. Ejecuta:
   ```sh
   docker-compose up --build
   ```
4. Accede a [http://localhost:8080](http://localhost:8080) en tu navegador.

## Crear un superusuario para el admin de Django

Para acceder al panel de administración de Django (`/admin`), necesitas un superusuario.  
Puedes crearlo así:

1. Abre una terminal y ejecuta:
   ```sh
   docker-compose run web python manage.py createsuperuser
   ```
2. Ingresa el nombre de usuario, correo y contraseña cuando se te solicite.
3. Ahora podrás iniciar sesión en [http://localhost:8080/admin](http://localhost:8080/admin) con esas credenciales.

## Notas

- Los archivos estáticos deben estar en `app/static/`.
- Los cambios en archivos CSS se reflejan automáticamente gracias al volumen de Docker.
- El panel de administración de Django está disponible en `/admin` (requiere superusuario).
- Solo los administradores pueden acceder al dashboard