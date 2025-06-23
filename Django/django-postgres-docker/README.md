# Django PostgreSQL Docker - Esqueleto Minimalista

Este proyecto es una configuración minimalista de Django con Docker y PostgreSQL. El esqueleto está diseñado para mostrar una página simple "¡Hola, Django desde Docker!" mientras mantiene la configuración de PostgreSQL para desarrollo futuro.

## Estructura del Proyecto

```
django-postgres-docker/
├── app/
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── migrations/
│   │   └── __init__.py
│   ├── models.py
│   ├── settings.py
│   ├── tests.py
│   ├── urls.py
│   ├── views.py
│   └── wsgi.py
├── docker-compose.yml
├── Dockerfile
├── manage.py
├── README.md
└── requirements.txt
```

## Requisitos Previos

- Docker y Docker Compose instalados en tu máquina.

## Instrucciones de Configuración

1. **Clonar el Repositorio**: Clona este repositorio en tu máquina local.

2. **Navegar al Directorio del Proyecto**:
   ```bash
   cd django-postgres-docker
   ```

3. **Construir los Contenedores Docker**:
   ```bash
   docker-compose build
   ```

4. **Ejecutar los Contenedores Docker**:
   ```bash
   docker-compose up
   ```

5. **Migrar la Base de Datos**:
   En una nueva terminal, ejecuta el siguiente comando para aplicar las migraciones:
   ```bash
   docker-compose run web python manage.py migrate
   ```

6. **Acceder a la Aplicación**:
   Abre tu navegador web y ve a `http://localhost:8080` para ver la aplicación Django en funcionamiento.

## Uso

- Para detener los contenedores, presiona `CTRL+C` en la terminal donde están ejecutándose.
- Para ejecutar los contenedores en segundo plano, usa:
  ```bash
  docker-compose up -d
  ```
- Para ver los logs cuando los contenedores están en segundo plano:
  ```bash
  docker-compose logs
  ```
- Para detener y eliminar los contenedores:
  ```bash
  docker-compose down
  ```

## Desarrollo Futuro

Este esqueleto está preparado para expandirse:

- El archivo `models.py` está listo para añadir modelos de base de datos.
- La configuración de PostgreSQL ya está en place para desarrollo de bases de datos relacionales.
- El archivo `admin.py` está preparado para registrar modelos en el panel de administración de Django.

## Personalización

Para modificar el mensaje mostrado, edita la función `index` en el archivo `app/views.py`.

## Notas

- La configuración actual expone la aplicación en el puerto 8080.
- Para cambiar la configuración de la base de datos, edita las variables de entorno en `docker-compose.yml`.
- Para añadir dependencias adicionales, actualiza el archivo `requirements.txt`.

## Licencia

Este proyecto está licenciado bajo la Licencia MIT.