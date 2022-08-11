# Intrucciones para correr prueba transacciones
Este proyecto hace calculo de transacciones a partir de un csv, hecho el calculo se envia un resumen por correo electronico
Por cuestion de seguridad se requiere una cuenta de google con doble factor de seguridad activado  y una contraseña
de aplicacion actividada en un archivo de variables de entorno.

## Requerimientos
Se utilizó python 3.10.4 y Ubuntu 22.04.1 LTS para su desarrollo.
Para mas detalles de los paquetes utilizados, consultar requirements.txt
Se aconseja el uso de contenedor Docker

## Probar el proyecto

## Sin uso de contenedor y con un ambiente virtual creado, solo se requiere ejecutar main.py.
```
virtualenv -p python3.10.4 test_stori
source test_stori/bin/activate
pip install -r requirements.txt 
python main.py
```

## Probar proyecto en un contenedor docker (Recomendado)
Con el engine de docker instalado, ejecutar a nivel de proyecto python:
```
docker build -t test_stori .
docker run -it -p 5432:5432 --rm --name test_stori test_stori
docker inspect --format '{{ .NetworkSettings.IPAddress }}' 0447aabb8d22
```
Nota: Puede ser necesario permisos de administrador (sudo)
El ultimo comando sirve para obtener la ip del contenedor de la BD, necesario
para llegar al contenedor de postgres desde el contenedor Python

## Docker database: postgresql

```
docker pull postgres:latest
sudo docker run -p 5432:5432 -e POSTGRES_PASSWORD=password postgres
```