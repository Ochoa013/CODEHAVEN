# Servicios profesionales — Desarrollo de software y asesoría legal

Sitio profesional construido con Django y adaptado sobre los recursos visuales de la plantilla existente. La portada permite elegir entre dos áreas: desarrollo de software bajo la identidad CODEHAVEN y asesoría legal.

## Páginas principales

- `/`: portada para elegir el servicio.
- `/desarrollo-web/`: página de desarrollo de software y formulario de cotización.
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

Cada solicitud se almacena primero en la base de datos. Después se envía una única notificación mediante Resend, exclusivamente a la dirección configurada en `CONTACT_EMAIL`.

La solicitud queda guardada aunque Resend esté temporalmente fuera de servicio, y el resultado se consulta desde Django Admin. El correo del cliente se utiliza únicamente como `reply_to` para facilitar la respuesta.

Las variables disponibles están documentadas en `.env.example`. Para desarrollo local, Django carga automáticamente el archivo `.env`, que está excluido de Git. En producción deben definirse como variables privadas del servicio de alojamiento.

Para Resend:

- `RESEND_API_KEY`, con la clave privada proporcionada por Resend.
- `RESEND_FROM_EMAIL`, con una dirección remitente autorizada por Resend.
- `CONTACT_EMAIL`, con el único destinatario de las solicitudes.

El dominio o la dirección remitente deben estar autorizados en Resend. El formulario mostrará la confirmación de éxito únicamente cuando Resend devuelva un identificador de envío.

No se deben copiar credenciales reales dentro de `settings.py`, plantillas o archivos versionados.

## Estructura principal

- `perfil_profesional/`: configuración y rutas del proyecto.
- `contacto/`: modelo, formulario, vistas, administración y pruebas.
- `templates/`: Home y página 404.
- `static/`: recursos originales de la plantilla y la adaptación visual.
- `db.sqlite3`: base de datos local con la estructura ya migrada.
