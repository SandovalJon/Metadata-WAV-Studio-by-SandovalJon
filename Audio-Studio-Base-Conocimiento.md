# Audio Studio — Base de Conocimiento

## 1. IDENTIDAD

- **Nombre**: Audio Studio
- **Descripción**: Editor de metadatos, conversor de audio y gestor de portadas. Funciona como PWA (Progressive Web App).
- **Stack**: HTML5, CSS3, JavaScript vanilla, sin frameworks.
- **Librerías externas**: jsmediatags (lectura ID3), browser-id3-writer (escritura ID3), lamejs (codificación MP3).
- **Backend**: Firebase (autenticación Google + Firestore para datos de usuario).
- **Repo**: https://github.com/SandovalJon/Metadata-WAV-Studio-by-SandovalJon
- **URL producción**: https://sandovaljon.github.io/Metadata-WAV-Studio-by-SandovalJon/
- **Versión actual**: v2.0.0
- **Fecha**: 2026-09-23

## 2. ARQUITECTURA

### Archivos
- `index.html` — Aplicación completa (HTML + CSS + JS inline)
- `sw.js` — Service Worker para funcionamiento offline
- `manifest.json` — Configuración PWA
- `icon-192.png` / `icon-512.png` — Iconos de la app

### Flujo principal
1. Usuario arrastra/selecciona archivo MP3 o WAV
2. Se leen metadatos existentes (ID3 para MP3, LIST-INFO para WAV)
3. Usuario edita campos en pestaña "Editar metadatos"
4. Usuario configura conversión en pestaña "Convertir audio"
5. Se genera y descarga el archivo resultante

### Pestañas
- **Editar metadatos**: Título, artista, álbum, año, pista, género, compositor, comentario, portada
- **Convertir audio**: Formato salida (MP3/WAV), bits, frecuencia, canales, normalizar, dithering, resampleo, presets

### Temas
- Oscuro (default, #0d1117)
- Claro (#f8f9fa)
- Esmeralda (solo usuario owner: jdss07@outlook.fr)

### Despliegue
- GitHub Pages desde rama `gh-pages`
- Service Worker con caché para offline

## 3. RECURSOS

### Firebase
- **apiKey**: AIzaSyAmy6B6r6xOk6tStMJHm0_-tJGeH7YrbZY
- **authDomain**: metadata---wav-studio.firebaseapp.com
- **projectId**: metadata---wav-studio
- **Usuario owner**: jdss07@outlook.fr

### APIs externas (CDN)
- jsmediatags: https://cdn.jsdelivr.net/npm/jsmediatags@3.9.7/dist/jsmediatags.min.js
- browser-id3-writer: https://cdn.jsdelivr.net/npm/browser-id3-writer@4.4.0/dist/browser-id3-writer.js
- lamejs: https://cdn.jsdelivr.net/npm/lamejs@1.2.1/lame.min.js
- Firebase: https://www.gstatic.com/firebasejs/10.12.2/

### localStorage keys
- `theme` — Tema seleccionado
- `lastTab` — Última pestaña usada
- `wavPresets` — Presets de conversión WAV
- `draftFields` — Borrador de campos
- `compactMode` — Modo compacto activado
- `windowSize` — Tamaño de ventana

## 4. CAPACIDADES

### Editor de metadatos
- **MP3**: Lee/escribe tags ID3v2 (TIT2, TPE1, TALB, TPE2, TYER, TRCK, TCON, TCOM, COMM, APIC)
- **WAV**: Lee/escribe LIST-INFO (INAM, IART, IPRD, ICRD, ITRK, IGNR, ICMT)
- **Portada**: Embebe imagen JPG/PNG en el archivo
- **Lote**: Procesa múltiples archivos a la vez

### Conversión de audio
- **MP3 → WAV**: Con configurable de bits (8-32 float), frecuencia (8000-192000 Hz), canales, normalizar, dithering, resampleo
- **WAV → MP3**: lamejs a 192kbps, estéreo, 44100Hz
- **WAV → WAV**: Re-guarda con metadatos LIST-INFO

### Presets
- Guardar configuración con nombre
- Cargar preset existente
- Resetear a valores mínimos
- Eliminar preset

### PWA
- Instalable en celular
- Offline después de primera carga
- Service Worker con caché de librerías

### Atajos de teclado
- Ctrl+G: Guardar y descargar
- Ctrl+L: Limpiar campos
- Ctrl+Z: Undo
- Ctrl+Y: Redo
- Ctrl+?: Modal de atajos
- Esc: Cerrar form

### UX
- 25 idiomas
- Temas (oscuro/claro/esmeralda)
- Drag & drop de archivos e imágenes
- Toast notifications
- Skeleton loading + barra de progreso
- Tooltips con tags ID3
- Contador de caracteres
- Modo compacto
- Doble click para resetear campo
- Click fuera del form para cerrar

## 5. LECCIONES

1. **display:none no funciona en option elements** — Los elementos `<option>` dentro de `<select>` no responden a `display:none`. Solución: agregar/quitar dinámicamente con `createElement`/`remove()`. Verificado: el select de temas no ocultaba Esmeralda.

2. **Service Worker cachea versiones viejas** — Cambiar el nombre del caché (v1 → v2) fuerza invalidación. Sin esto, el usuario ve la versión anterior tras refresh normal.

3. **Service Worker puede bloquear actualizaciones** — Si el SW viejo tiene cacheado el index.html viejo, el código nuevo nunca ejecuta. Solución: desregistrar SW viejo o usar nombre de caché nuevo.

4. **position:fixed en footer impide scroll natural** — Usar flexbox en body con `flex:1` en main es mejor para footer siempre al fondo.

5. **flex:1 en button CSS global afecta todos los botones** — Los botones inline con estilos específicos necesitan `flex:0 0 auto` para sobreescribir.

6. **GitHub Pages subdirectorio** — Las rutas absolutas (/) no funcionan en subdirectorios. Usar rutas relativas (./) o absolutas con el subdirectorio (/Metadata-WAV-Studio-by-SandovalJon/).

7. **WAV metadata enLIST-INFO** — Los campos se mapean: INAM=title, IART=artist, IPRD=album, ICRD=year, ITRK=track, IGNR=genre, ICMT=comment.

8. **Dithering reduce ruido de cuantización** — TPDF es el estándar para música. Sin dither al bajar de 24→16 bits se genera ruido audible.

9. **Plataformas comprimen el audio** — Spotify, Apple Music, YouTube convierten todo. Subir 32-bit/192kHz es inútil; 24-bit/48kHz es el óptimo.

10. **PWA en GitHub Pages requiere paths absolutos** — El scope y start_url deben incluir el subdirectorio completo para que la instalación funcione correctamente.
