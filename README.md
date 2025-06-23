# Django Proyect IS
proyecto sobre  pagina web de ingenieria en software 

paso 1 abrir docker en la terminal de la carpeta raiz escribir :

docker-compose run web python manage.py migrate

docker-compose exec web python manage.py makemigrations
docker-compose exec web python manage.py migrate

despues escribir: 
docker-compose up --build

ir al localhost8080