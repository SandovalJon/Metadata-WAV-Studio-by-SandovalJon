# Metadata-Manual-Skills.md

## Ficha

| Campo | Valor |
|---|---|
| Nombre | Metadata & WAV Studio |
| Tipo | Pagina web client-side (single-file) |
| Archivo | `index.html` |
| Stack | HTML + CSS + JS vanilla, jsmediatags, browser-id3-writer, Web Audio API |
| Repo | https://github.com/SandovalJon/Metadata.git |
| Branch | master |
| Version | v1 (2026-09-19) |

## Arquitectura y flujo

- Un solo archivo `index.html` (aprox. 830 lineas, 27 KB).
- Tema oscuro con CSS custom properties.
- IIFE en JS para encapsular estado (no hay globals).
- Flujo: el usuario carga un MP3, edita metadatos, elige formato de salida (MP3 o WAV), configura opciones, descarga el resultado.
- Las dependencias se cargan desde CDN al abrir la pagina (no hay build, no hay servidor).
- La conversion WAV usa `OfflineAudioContext` para remuestrear y cambiar canales; el encoder WAV esta implementado en vanilla JS.

## Capacidades

1. **Leer metadatos MP3** — titulo, artista, album, artista del album, anio, pista, genero, compositor, comentario, portada existente.
2. **Editar metadatos MP3** — todos los campos de texto editables.
3. **Portada** — agregar/quitar con drag & drop o selector de archivos. Boton visible "Anadir o arrastrar portada aqui".
4. **Eliminar imagenes viejas** — cleanAudio() elimina todas las ID3 (inicio, final) e ID3v1 antes de escribir. Solo queda la portada nueva si se agrega una.
5. **Guardar MP3** — descarga el archivo con las nuevas tags ID3.
6. **Convertir MP3 a WAV** — decodifica, remuestrea, cambia canales, normaliza, codifica WAV con metadata LIST/INFO.
7. **Configuracion de conversion** — bits (8/16/24/32int/32float), frecuencia (8k-192k Hz), canales (mono/estereo), normalizacion (auto/none/max).
8. **Tamano** — muestra tamano original vs resultado; para WAV muestra estimado por minuto.

## APIs, claves y recursos

- **jsmediatags@3.9.7** — CDN: `https://cdn.jsdelivr.net/npm/jsmediatags@3.9.7/dist/jsmediatags.min.js` — lectura de tags ID3.
- **browser-id3-writer@4.4.0** — CDN: `https://cdn.jsdelivr.net/npm/browser-id3-writer@4.4.0/dist/browser-id3-writer.js` — escritura de tags ID3. Solo acepta ArrayBuffer como primer argumento. Frames multiples (TPE1, TPE2, TCOM) requieren array de strings.
- **Web Audio API** — nativa del navegador. `decodeAudioData` decodifica MP3 a AudioBuffer. `OfflineAudioContext` permite renderizar a otra frecuencia/canales.
- **No hay claves ni endpoints.** Todo es local y offline.

## Datos y memoria

- No hay base de datos, localStorage ni estado persistente. Todo es ephemeral (se carga en memoria, se descarga, se pierde).
- Tags ID3 editables: TIT2, TPE1, TALB, TPE2, TYER, TRCK, TCON, TCOM, COMM, APIC.
- Tags WAV (LIST INFO): INAM, IART, IPRD, ICRD, ITRK, IGNR, ICMT.
- Variables de estado JS: `currentFile`, `originalTags`, `coverBlob`, `coverPending`, `originalSize`.

## Despliegue y operacion

- **Local**: Abrir `index.html` en navegador. Requiere conexion a internet la primera vez (para cargar CDN). Despues puede funcionar offline si el cache del navegador lo permite.
- **GitHub Pages**: Activar en Settings > Pages > Source: master. URL: `https://sandovaljon.github.io/Metadata/`.
- **No hay build ni servidor.** No hay comandos npm, no hay deploy script.
- **Git**: `git add . && git commit -m "mensaje" && git push origin master`.

## Skills y lecciones

1. **ID3Writer y ArrayBuffer** — browser-id3-writer solo acepta ArrayBuffer. Siempre convertir con `file.arrayBuffer()`.
2. **Frames multiples** — TPE1, TPE2, TCOM, etc. requieren array: `['valor']`, no `'valor'`.
3. **Race condition** — `coverPending` debe resolverse antes del guardado. Usar `await coverPending` en submit.
4. **Limpieza de tags** — `cleanAudio()` elimina todas las ID3 (inicio + final) e ID3v1. La imagen original siempre se elimina.
5. **CSS file input** — `input[type="file"] { display: none }` oculta todos los file inputs. Usar boton dedicado que dispare el input oculto.
6. **Clamp en int** — Siempre clampear samples antes de escribir a PCM int para evitar overflow.
7. **Frecuencias altas** — 192k puede fallar en algunos navegadores. Ofrecer fallback a 96k.

## Estado y pendientes

- **Version actual**: v1 (2026-09-19, commit `527d11a`)
- **Funcionalidad completa**: Editor de metadatos + convertidor WAV funcional.
- **Pendientes (ideas)**:
  - Soporte para mas formatos de entrada (M4A, FLAC, OGG).
  - Soporte para metadatos en WAV de salida (actual: LIST/INFO basico).
  - Soporte para portada en archivos FLAC/OGG.
  - Editor de waveform visual.
  - Soporte para lotes (varios archivos a la vez).
  - Dithering configurable para 16/8 bits.
