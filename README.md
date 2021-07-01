# ecommercePolotic
Trabajo Integrador Curso PYTHON Y JAVASCRIPT - Polotic - Misiones - Argentina

# Modulos: 

Inicio y Cierre de Sesion 
Alta de Usuarios 
CRUD de Categorias 
CRUD Productos 
CRUD Carrito

# BASE DE DATOS:

Se utiliza la BD por defecto de Django, SQLITE3

# ENTORNO VIRTUAL del Proyecto

Crear un entorno virtual al nivel de la carpeta app con el siguiente comando:

python3 -m venv venv

Luego acceder a "RAIZ Proyecto"/venv/bin y ejecutar:

source bin/ activate #Para activar el entorno virtual

# LIBRERIAS NECESARIAS del Proyecto

Luego ejecutar lo siguiente para instalar las librerias necesarias:

pip install Django==3.2.4 #Para instalar django en el entorno virtual 
pip install django-widget-tweaks==1.4.8 #Libreria necesaria para el proyecto.
pip install Pillow==8.2.0 #Para poder utilizar imagenes en el proyecto

Otra alternativa es en vez de ejecutar lo anterior, podemos ejecutar el comando siguiente en la terminal, despues de activado el entorno virtual:

accedemos a la carpeta app/

ejecutamos:

pip install -r requirements.txt

# PARA EJECUTAR EL PROYECTO

Ubicarse dentro de la carpeta app/

Ejecutar el siguiente comando:

python3 manage.py runserver

Luego acceder a:

http://127.0.0.1:8000

Para poder usar el proyecto en modo SUPERUSER ingresar con el siguiente usuario y contraseña:

SuperUsuario: moderador Contraseña: ninguna

Usuarios comunes:

Usuario: usuario Contraseña: usuario2021

El proyecto fue realizado con las siguiente tecnologías:

Python 3.8.5 -- Django 3.2.4 -- Bootstrap 4 -- Template AdminLTE 3.0.4
