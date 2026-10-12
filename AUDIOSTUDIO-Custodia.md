# AUDIOSTUDIO — Custodia del Proyecto

> Última actualización: 2026-10-12 · Versión del documento: v1

## Mapa del documento

Lectura por defecto: `7. MEMORIA` y este mapa. Las secciones `1`–`5` se abren **solo** cuando la tarea las mencione (`4. CAPACIDADES` y `5. LECCIONES` son de consulta).

- mp3, id3, id3v2, tags, portada, metadatos → `4. CAPACIDADES`
- wav, riff, list-info, bloques, cabecera, duracion → `4. CAPACIDADES`
- procesar por lotes, varios archivos, renombrar → `4. CAPACIDADES`
- pwa, sw.js, cache, manifest, offline → `2. ARQUITECTURA`
- que es el proyecto, stack, rutas, repo, URL de Pages → `1. IDENTIDAD`
- por que algo se hizo asi, gotchas, errores del pasado → `5. LECCIONES`
- como validar, desplegar, ver logs → `6. SKILLS`
- estado actual, decisiones, tarea activa → `7. MEMORIA`
- historial de cambios → `8. VERSIONES` (solo visibles; `8b` nunca)
- entradas antiguas → `5b` / `8b`

## 1. IDENTIDAD

- Qué es el proyecto: editor de metadatos de audio y conversor de MP3/WAV, con gestión de portadas. Lee y escribe etiquetas ID3v2 en MP3 y bloques LIST-INFO en WAV, convierte entre formatos y incrusta carátulas. Funciona como PWA instalable y sin conexión.
- Stack: HTML5, CSS3 y JavaScript vanilla, sin frameworks ni build. `index.html` concentra toda la aplicación con 3.627 líneas.
- Rutas principales: `index.html` (aplicación completa), `sw.js` (service worker), `manifest.json` (PWA), `icon-192.png` y `icon-512.png`. Este documento: `AUDIOSTUDIO-Custodia.md`.
- Repo git y estado: el remoto local apunta a `https://github.com/SandovalJon/Metadata.git`, pero ese nombre fue renombrado: la API devuelve el mismo repositorio bajo `Metadata-WAV-Studio-by-SandovalJon` (id `1377353179`). Rama por defecto `master`; existen `origin/master` y `origin/gh-pages`. `git status` limpio en el momento de la migración.
- URLs: `https://sandovaljon.github.io/Metadata-WAV-Studio-by-SandovalJon/`. Repositorio: `https://github.com/SandovalJon/Metadata-WAV-Studio-by-SandovalJon`.
- Versión del código: `8eb519c` ("v3.1.0", 2026-10-04). La versión visible en la app es `v3.1.0` (`index.html`, línea 850).
- Fecha de la última versión del código: 2026-10-04.

## 2. ARQUITECTURA

- Componentes: aplicación de archivo único más los artefactos de PWA. `sw.js` precarga el propio servicio, sus iconos y las cuatro librerías externas que la app necesita.
- Cómo se conectan: Firebase aporta autenticación con Google y Firestore para datos de usuario. Las librerías de audio llegan por CDN y quedan cacheadas por el service worker para el uso sin conexión.
- Entry points: `index.html`. GitHub Pages se construye desde la rama `gh-pages`, no desde `master`.
- Flujos clave:
  1. El usuario arrastra o selecciona uno o varios archivos MP3 o WAV.
  2. Se leen los metadatos existentes: ID3v2 en MP3, LIST-INFO en WAV.
  3. En la pestaña "Editar metadatos" se modifican los campos y se adjunta la portada.
  4. En la pestaña "Convertir audio" se elige formato de salida, profundidad, frecuencia, canales, normalización, dithering y resampleo.
  5. Se genera y descarga el archivo resultante.
- Temas: oscuro por defecto (`#0d1117`), claro (`#f8f9fa`) y Esmeralda, este último restringido a la cuenta de propietario definida en el código.
- Despliegue (comandos exactos): `git add -A && git commit -m "Mensaje" && git push origin master` y a continuación `git checkout gh-pages && git merge master && git push origin gh-pages && git checkout master`. Subir el número de caché en `sw.js` dentro del mismo despliegue. Pages construye desde `gh-pages`.
- Operación (comandos exactos): estado del sitio con `gh api repos/SandovalJon/Metadata-WAV-Studio-by-SandovalJon/pages --jq '{branch: .source.branch, status: .status}'`. Forzar actualización en el navegador con `Ctrl+Shift+R` o borrando los datos del sitio.

## 3. RECURSOS

- APIs que usa:
  - jsmediatags 3.9.7 (lectura de ID3), `cdn.jsdelivr.net`.
  - browser-id3-writer 4.4.0 (escritura de ID3), `cdn.jsdelivr.net`.
  - lamejs 1.2.1 (codificación MP3), `cdn.jsdelivr.net`.
  - Firebase 10.12.2, autenticación y Firestore desde `gstatic`.
- Dónde vive la configuración: la configuración de Firebase (clave de API, dominio de autenticación e identificador de proyecto) está incrustada en `index.html`, líneas 2528 a 2530. El identificador de la cuenta propietaria que habilita el tema Esmeralda también está en el código. No hay variables de entorno ni archivo de configuración aparte.
- Aviso de privacidad: esta sección referencia configuración sensible. Uso local. No subir a repos.
- Esquemas de datos: mapeo de ID3v2 en MP3: TIT2 título, TPE1 artista, TALB álbum, TPE2 artista del álbum, TYER año, TRCK pista, TCON género, TCOM compositor, COMM comentario, APIC portada. Mapeo de LIST-INFO en WAV: INAM título, IART artista, IPRD álbum, ICRD año, ITRK pista, IGNR género, ICMT comentario.
- Memoria / almacenamiento: claves de `localStorage`: `theme`, `lastTab`, `wavPresets`, `draftFields`, `compactMode` y `windowSize`. Sin IndexedDB.

## 4. CAPACIDADES

- Editor de metadatos MP3 — lee y escribe ID3v2 con los diez campos y portada incrustada. Verificado por: código y documentación heredada.
- Editor de metadatos WAV — lee y escribe los siete bloques LIST-INFO. Verificado por: código y documentación heredada.
- Procesamiento por lotes — varios archivos en una sola operación. Verificado por: código y documentación heredada.
- Conversión MP3 a WAV — configurable en profundidad de bits (8, 16, 24, 32 y 32 float), frecuencia de 8.000 a 192.000 Hz, canales mono o estéreo, normalización (ninguna, automática a -1 dB o máxima a 0 dB), dithering (ninguno, TPDF o high pass) y resampleo (bajo, medio, alto). Verificado por: código y documentación heredada.
- Conversión WAV a MP3 — con lamejs a 192 kbps, estéreo y 44.100 Hz. Verificado por: código y documentación heredada.
- Conversión WAV a WAV — reescribe el archivo conservando los metadatos LIST-INFO. Verificado por: código y documentación heredada.
- Portada — incrusta o quita imagen JPG/PNG dentro del archivo. Verificado por: código y documentación heredada.
- Presets de conversión — guardar con nombre, cargar, restablecer a valores mínimos y eliminar. Se guardan en `localStorage` bajo `wavPresets`. Verificado por: código y documentación heredada.
- PWA — instalable, funciona sin conexión tras la primera carga y cachea las librerías. Verificado por: `sw.js` precarga seis recursos; la instalación no está verificada en dispositivo.
- Atajos de teclado — `Ctrl+G` guarda y descarga, `Ctrl+L` limpia campos, `Ctrl+Z` deshace, `Ctrl+Y` rehace, `Ctrl+?` abre el modal de atajos y `Esc` cierra el formulario. Verificado por: documentación heredada.
- Interfaz — 25 idiomas, tres temas, arrastrar y soltar para archivos e imágenes, avisos flotantes, esqueletos de carga, barra de progreso, descripciones de etiquetas ID3, contador de caracteres, modo compacto, doble clic para restablecer un campo y cierre del formulario al hacer clic fuera. Verificado por: documentación heredada.

## 5. LECCIONES

1. `display:none` no funciona en elementos `<option>` — Causa raíz: los `<option>` dentro de un `<select>` ignoran `display:none`, así que el tema Esmeralda seguía visible. · Fix: agregar y quitar dinámicamente con `createElement` y `remove()`. · Verificación: el selector de temas deja de mostrar Esmeralda a quien no debe.
2. El service worker sigue sirviendo la versión anterior — Causa raíz: la caché con nombre fijo sobrevive a los despliegues. · Fix: renombrar la caché en cada despliegue; actualmente `audio-studio-v4` en `sw.js`. · Verificación: el banner de nueva versión aparece tras desplegar.
3. Un service worker antiguo puede bloquear la actualización por completo — Causa raíz: si el SW viejo tiene cacheado el `index.html` viejo, el código nuevo nunca llega a ejecutarse. · Fix: usar un nombre de caché nuevo o desregistrar el SW previo. · Verificación: actualizar con `Ctrl+Shift+R` o borrando datos del sitio.
4. `position: fixed` en el footer impide el scroll natural — Causa raíz: el footer queda fuera del flujo y solapa el contenido. · Fix: flexbox en `body` con `flex:1` en `main` para empujar el footer al fondo. · Verificación: el scroll llega al final de listas largas.
5. `flex:1` en un botón de CSS global afecta a todos los botones — Causa raíz: una regla amplia se propaga a botones inline con estilos propios. · Fix: sobreescribir con `flex:0 0 auto` donde haga falta. · Verificación: los botones conservan su ancho.
6. En un subdirectorio de GitHub Pages las rutas absolutas no funcionan — Causa raíz: una ruta que empieza por `/` apunta a la raíz del dominio, no al proyecto. · Fix: usar rutas relativas `./` o absolutas incluyendo el subdirectorio completo. · Verificación: la app carga desde su subdirectorio.
7. El alcance de la PWA en GitHub Pages debe llevar el subdirectorio — Causa raíz: si `scope` y `start_url` no incluyen el subdirectorio, la instalación falla o apunta a la raíz del dominio. · Fix: declarar el subdirectorio completo en el manifiesto. · Verificación: instalar desde el sitio publicado.
8. Los bloques LIST-INFO del WAV se mapean por identificador corto — Causa raíz: cada campo tiene un identificador fijo y no un nombre legible. · Fix: INAM título, IART artista, IPRD álbum, ICRD año, ITRK pista, IGNR género, ICMT comentario. · Verificación: lectura y escritura de los siete campos.
9. El dithering evita ruido de cuantización — Causa raíz: al bajar de 24 a 16 bits aparece ruido audible sin dithering. · Fix: usar TPDF, el estándar para música. · Verificación: conversión a 16 bits sin zumbido.
10. Subir resolución de audio por encima de 24 bits y 48 kHz es inútil — Causa raíz: Spotify, Apple Music y YouTube recomprimen todo lo que publican. · Fix: 24 bits y 48 kHz es el punto óptimo. · Verificación: no verificado.
11. La versión de la app y la del service worker se desincronizan — Causa raíz: la app declara `v3.1.0` en `index.html:850` mientras `sw.js` declara `VERSION = 'v2.1.0'` y caché `audio-studio-v4`; nadie sincronizó ambas tras las últimas entregas. · Fix: derivar la versión del service worker de la de la app, o declararlas juntas en un único punto. · Verificación: comparación directa de ambos ficheros, realizada el 2026-10-12.
12. Documentar credenciales en Markdown las filtra a los repos — Causa raíz: el archivo heredado contenía la clave de API de Firebase en texto plano, y el repositorio es público. · Fix: este documento registra solo dónde vive la configuración y lleva el aviso de privacidad; el valor no se copia nunca. · Verificación: la sección `3. RECURSOS` de este archivo no contiene ninguna clave.

## 5b. LECCIONES (archivo)

Sin entradas archivadas todavía.

## 6. SKILLS

- Skill: desplegar con la rama `gh-pages` — Estado: verificada
  - Propósito: publicar cambios en el sitio sin romper el service worker.
  - Precondiciones: cambios commiteados en `master`.
  - Pasos: `git add -A && git commit -m "Mensaje" && git push origin master` · subir el número de caché en `sw.js` dentro del mismo commit · `git checkout gh-pages && git merge master && git push origin gh-pages && git checkout master` · comprobar `gh api repos/SandovalJon/Metadata-WAV-Studio-by-SandovalJon/pages --jq '.status'` hasta `built`.
  - Verificación: Pages construye desde `gh-pages`, confirmado en la API; `origin/gh-pages` existe en el remoto.
  - Agente: [opencode-1]

- Skill: invalidar la caché del service worker — Estado: verificada
  - Propósito: forzar a los clientes a recibir la versión nueva.
  - Pasos: cambiar `const CACHE` en `sw.js` al valor siguiente · desplegar · en el navegador usar `Ctrl+Shift+R` o borrar los datos del sitio.
  - Verificación: el valor actual es `audio-studio-v4`, leído de `sw.js`.
  - Agente: [opencode-1]

- Skill: editar y escribir etiquetas de audio — Estado: pendiente de verificación
  - Propósito: capacidad técnica del proyecto, heredada de la documentación anterior sin comandos de comprobación.
  - Precondiciones: jsmediatags para lectura, browser-id3-writer para escritura de ID3, lamejs para MP3.
  - Pasos: leer el mapa de campos de la sección `3. RECURSOS` · usar `createElement` y `remove()` para opciones en lugar de `display:none` · convertir a 16 bits solo con dithering TPDF.
  - Verificación: pendiente. No hay suite de pruebas en este repositorio.
  - Agente: [opencode-1]

## 7. MEMORIA

- [opencode-1] Tarea activa: ninguna. Migración Ruta B ejecutada el 2026-10-12: se unificaron `Audio-Studio-Base-Conocimiento.md` y `Audio-Studio-Manual-Skills.md` en este archivo, y los originales quedaron en `archivados/` (locales, fuera del repo por contener credenciales).
- [opencode-1] Resuelto en v2: `sw.js` declaraba `VERSION = 'v2.1.0'` frente a una app en `v3.1.0`. Alineados y subida la caché a `audio-studio-v5`. La lección 5 nº 11 queda resuelta en la práctica.
- [opencode-1] Resuelto sin intervención: el remoto local apuntaba a `Metadata`, pero el push a `master` actualizó solo la URL al nombre actual `Metadata-WAV-Studio-by-SandovalJon`, porque Git detecta el renombrado en el servidor y reescribe el remoto. Verificado con `git remote get-url origin`.
- [opencode-1] Corregido: la documentación heredada declaraba versión `v2.0.0` del 2026-09-23 y caché `audio-studio-v2`; el código real es `v3.1.0` en `index.html:850`, commit `8eb519c`. Se adoptó lo verificado.
- [opencode-1] Hallazgo: el archivo heredado contenía la clave de API de Firebase en texto plano y el repositorio es público. El valor no se ha copiado a este documento, que solo indica dónde vive la configuración.
- [opencode-1] Pendiente abierto: borrar el repositorio `wallpaper-quest`, que requiere que el usuario autorice `gh auth refresh -h github.com -s delete_repo`. Fuera del alcance de este proyecto.
- [opencode-1] Decisión: `NOMBRE` es `AUDIOSTUDIO` — motivo: la carpeta y el repo describen el proyecto como "Metadata / WAV Studio", pero el nombre real de la aplicación en `manifest.json` y en la documentación heredada es "Audio Studio" — estado: tomada.
- [opencode-1] Decisión: Pages se despliega desde `gh-pages` y no desde `master` — motivo: así consta en la configuración de Pages y en el procedimiento heredado — estado: tomada.
- Preferencias del usuario: español; respuestas concisas; un archivo de custodia por página; quiere que el agente ejecute y publique sin pedir confirmación paso a paso.
- Comprometidos: Firebase Auth y Firestore siguen siendo dependencias para la parte de datos de usuario. El tema Esmeralda está restringido a la cuenta de propietario.
- Ideas (no comprometidos): deshacer/rehacer global, modo oscuro automático, exportar configuración a JSON, copiar metadatos al portapapeles, efecto ripple, partículas de fondo, buscar en la lista de idiomas y recordar el tamaño de ventana. Ninguna comprometida.

## 8. VERSIONES

- v1 | 2026-10-12 | Migración Ruta B a documento único | código: 8eb519c
  - Agente: [opencode-1]
  - Qué cambió: se unificaron `Audio-Studio-Base-Conocimiento.md` y `Audio-Studio-Manual-Skills.md` en este archivo de custodia. Se corrigieron dos datos desactualizados heredados: la versión pasa de `v2.0.0` a `v3.1.0` y la caché del service worker de `audio-studio-v2` a `audio-studio-v4`. Se retiraron del documento los valores de credenciales que la documentación anterior exponía en texto plano. No se modificó código de la app.
  - Secciones actualizadas: todas (creación por migración). `3. RECURSOS` incorpora el aviso de privacidad y elimina la clave. `5. LECCIONES` consolida las dieciséis entradas heredadas en doce sin duplicar y añade dos nuevas: el desfase de versión con el service worker y la filtración de credenciales en Markdown. `6. SKILLS` registra el despliegue por `gh-pages` y la invalidación de caché.
  - Verificación: versión leída de `index.html:850`; `git log -1` da `8eb519c`; la API de Pages devuelve rama `gh-pages` y estado `built`; `sw.js` declara `CACHE = 'audio-studio-v4'` y `VERSION = 'v2.1.0'`; la configuración de Firebase está en `index.html` líneas 2528-2530; `git branch -r` muestra `origin/master` y `origin/gh-pages`; el repositorio es público y su id es `1377353179`.
  - Pendientes: actualizar el remoto local de `Metadata` a `Metadata-WAV-Studio-by-SandovalJon`; sincronizar `VERSION` de `sw.js` con la versión de la app; decidir si la clave de API de Firebase debe rotarse por haber estado documentada en un repositorio público.

- v2 | 2026-10-12 | Sincronizar versión del service worker con la app | código: sin-commit
  - Agente: [opencode-1]
  - Qué cambió: `sw.js` pasa de `VERSION = 'v2.1.0'` a `VERSION = 'v3.1.0'`, alineado con la versión que la app declara en `index.html:850`. La caché sube de `audio-studio-v4` a `audio-studio-v5`, siguiendo el procedimiento propio del proyecto para invalidar la caché de los clientes. Es el único cambio de código; la app no se vio afectada.
  - Secciones actualizadas: `7. MEMORIA` marca la lección 5 nº 11 como resuelta y el remoto local como resuelto por el propio push. La lección 5 nº 11 se deja sin reescribir, como manda el append-only.
  - Verificación: `node --check sw.js` sin errores; `sw.js` declara `CACHE = 'audio-studio-v5'` y `VERSION = 'v3.1.0'`; `index.html:850` declara `v3.1.0`. Pendiente de verificar el resultado tras el despliegue: el banner de nueva versión en un cliente con la versión anterior y que el sitio siga respondiendo.
  - Pendientes: rotar la clave de API de Firebase, que sigue presente en el historial de git aunque ya no esté en la raíz del repositorio.

## 8b. VERSIONES (archivo)

Sin entradas archivadas todavía.