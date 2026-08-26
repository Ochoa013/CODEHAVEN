# Servicios profesionales — Desarrollo de software y asesoría legal

Sitio profesional construido con Django y adaptado sobre los recursos visuales de la plantilla existente. La portada permite elegir entre dos áreas: desarrollo de software bajo la identidad CODEHAVEN y asesoría legal.

## Páginas principales

- `/`: portada para elegir el servicio.
- `/desarrollo-web/`: página de desarrollo de software y contacto directo por WhatsApp.
- `/asesoria-legal/`: página informativa de asesoría legal y contacto por WhatsApp.

## Ejecución local

Desde esta carpeta:

```powershell
python manage.py runserver
```

La base de datos y las migraciones iniciales ya están preparadas. Si el proyecto se copia a otra ubicación, se pueden aplicar nuevamente con:

```powershell
python manage.py migrate
```

## Administración de solicitudes históricas

Crear el primer usuario administrador:

```powershell
python manage.py createsuperuser
```

Después, ingresar en `http://127.0.0.1:8000/admin/` para consultar las solicitudes registradas antes de retirar el formulario público.

## Comprobaciones

```powershell
python manage.py check
python manage.py test
```

## Configuración de producción

Antes de publicar la aplicación, definir estas variables del sistema:

- `DJANGO_DEBUG=False`
- `DJANGO_SECRET_KEY` con una clave privada larga y aleatoria
- `DJANGO_ALLOWED_HOSTS` con los dominios autorizados separados por comas
- `DJANGO_CSRF_TRUSTED_ORIGINS` con los orígenes HTTPS autorizados, separados por comas

La configuración de producción activa redirección HTTPS, cookies seguras, HSTS y cabeceras de protección. El archivo local `.django-secret-key` se genera únicamente para desarrollo y está excluido del control de versiones.

## Contacto

Desarrollo de software y asesoría legal utilizan WhatsApp como único canal público de contacto. Cada página abre una conversación con un mensaje inicial adaptado al servicio seleccionado.

## Estructura principal

- `perfil_profesional/`: configuración y rutas del proyecto.
- `contacto/`: vistas, administración, datos históricos y pruebas.
- `templates/`: Home y página 404.
- `static/`: recursos originales de la plantilla y la adaptación visual.
- `db.sqlite3`: base de datos local con la estructura ya migrada.
