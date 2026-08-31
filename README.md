# Sitio profesional de Esteban Ochoa

Sitio web estático, listo para publicarse en **GitHub Pages**. No requiere Django, base de datos, instalación de paquetes ni servidor: basta con abrir `index.html` o subir el contenido del repositorio a GitHub.

## Páginas incluidas

- `index.html`: portada para elegir el área de atención.
- `desarrollo-web.html`: servicios de desarrollo de software y soluciones digitales.
- `asesoria-legal.html`: servicios de asesoría legal.
- `perfil-profesional.html`: formación, herramientas tecnológicas y áreas jurídicas de Esteban Ochoa.
- `404.html`: página de error para GitHub Pages.

Todos los enlaces internos, el menú móvil y los botones de WhatsApp funcionan de manera estática. El sitio no tiene formularios ni correo: el contacto se realiza únicamente por WhatsApp, con mensajes predeterminados según el servicio. Así funciona también en GitHub Pages, donde no hay backend.

## Colocar tu foto

1. Copia tu foto a `assets/img/`.
2. Nómbrala exactamente `foto-perfil.png`.
3. Sube el archivo junto con los demás cambios.

La foto `assets/img/foto-perfil.png` ya está colocada en la portada y en las dos páginas de servicio. Si necesitas cambiarla más adelante, reemplaza ese archivo por otra imagen PNG con el mismo nombre.

Si prefieres JPG o WebP, cambia `foto-perfil.png` por el nombre de tu archivo en los tres HTML: `index.html`, `desarrollo-web.html` y `asesoria-legal.html`.

## Publicarlo en GitHub Pages

1. Crea un repositorio en GitHub y sube el contenido de esta carpeta.
2. En el repositorio, abre **Settings → Pages**.
3. En **Build and deployment**, selecciona **Deploy from a branch**.
4. Elige la rama `main` (o `master`) y la carpeta `/ (root)`.
5. Guarda los cambios y espera a que GitHub muestre la dirección pública del sitio.

El archivo `.nojekyll` está incluido para que GitHub Pages publique los recursos estáticos tal como están.

## Personalizaciones rápidas

- El número de WhatsApp actual es `+593 96 904 8598`. Para cambiarlo, busca `593969048598` en los archivos HTML y en `assets/js/main.js`.
- Los textos de los servicios están directamente en los tres archivos HTML.
- Los estilos están centralizados en `assets/css/styles.css`.

## Vista local

Haz doble clic en `index.html` para abrir el sitio en tu navegador. No necesitas ejecutar `python manage.py runserver`.
