# CODEHAVEN — Desarrollo de software

Sitio profesional de servicios de desarrollo de software construido con Django y adaptado sobre los recursos visuales de la plantilla existente.

## Ejecución local

Desde esta carpeta:

```powershell
python manage.py runserver
```

La base de datos y las migraciones iniciales ya están preparadas. Si el proyecto se copia a otra ubicación, se pueden aplicar nuevamente con:

```powershell
python manage.py migrate
```

## Administración de solicitudes

Crear el primer usuario administrador:

```powershell
python manage.py createsuperuser
```

Después, ingresar en `http://127.0.0.1:8000/admin/` para consultar, buscar, filtrar y actualizar el estado de las solicitudes.

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

## Notificaciones de cotización

Cada solicitud se almacena primero en la base de datos. Después se envía una única notificación a `ochoaesteban593@gmail.com` exclusivamente mediante Gmail SMTP.

La solicitud queda guardada aunque Gmail esté temporalmente fuera de servicio, y el resultado se consulta desde Django Admin.

Las variables disponibles están documentadas en `.env.example`. Para desarrollo local, Django carga automáticamente el archivo `.env`, que está excluido de Git. En producción deben definirse como variables privadas del servicio de alojamiento.

Para Gmail SMTP:

- `EMAIL_HOST_USER=ochoaesteban593@gmail.com`
- `EMAIL_HOST_PASSWORD`, usando una contraseña de aplicación de Google
- `DEFAULT_FROM_EMAIL=CODEHAVEN <ochoaesteban593@gmail.com>`
- `COTIZACIONES_EMAIL=ochoaesteban593@gmail.com`

Para activar el envío local solo debes completar `EMAIL_HOST_PASSWORD` en `.env`. La cuenta de Google debe tener verificación en dos pasos y una contraseña de aplicación habilitada.

No se deben copiar credenciales reales dentro de `settings.py`, plantillas o archivos versionados.

## Estructura principal

- `perfil_profesional/`: configuración y rutas del proyecto.
- `contacto/`: modelo, formulario, vistas, administración y pruebas.
- `templates/`: Home y página 404.
- `static/`: recursos originales de la plantilla y la adaptación visual.
- `db.sqlite3`: base de datos local con la estructura ya migrada.
