# Crear entorno virtual
python3 -m venv myvenv
python -m pip install --upgrade pip
# activate venv
cd path/to/directory
myenv\Scripts\activate

# Crer proyecto en Django
django-admin.exe startproject mysite .
# Crear una aplicacion
python manage.py startapp blog

# Crear base de datos
python manage.py migrate

# Crear tabalas para los modelos en la base de datos
python manage.py makemigrations blog
python manage.py migrate blog

# Administrar BBDD
python manage.py createsuperuser

# Iniciar Servidor
python manage.py runserver

# Desplegar
1. Subir a Github
2. Sincronizar pythonanywhere con github:
    - pa_autoconfigure_django.py --python=3.6 https://github.com/<your-github-username>/my-first-blog.git
2. git pull en pythonanywhere
3. Crear usuario en la bbdd del servidor python manage.py createsuperuser