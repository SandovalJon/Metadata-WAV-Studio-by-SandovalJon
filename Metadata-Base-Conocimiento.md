# Metadata-Base-Conocimiento.md (v1)

## 1. IDENTIDAD

- **Nombre**: Metadata & WAV Studio
- **Qué es**: Pagina web 100% client-side (single-file HTML) que sirve como editor de metadatos MP3 y convertidor MP3 a WAV con opciones avanzadas de audio.
- **Stack**: HTML + CSS + JavaScript vanilla, librerias externas via CDN: jsmediatags (lectura ID3), browser-id3-writer (escritura ID3), Web Audio API + OfflineAudioContext (conversion WAV).
- **Ruta**: `C:\SandovalJon\NO BORRAR\OpenCode\Metadata\`
- **Unico archivo**: `index.html` (27.8 KB, ~830 lineas)
- **Repo**: https://github.com/SandovalJon/Metadata.git
- **Branch**: master
- **Ultimo commit**: `527d11a` (Metadata & WAV Studio - editor de metadatos y convertidor MP3 a WAV)
- **Version actual**: v1
- **Fecha**: 2026-09-19
- **GitHub Pages**: pendiente de activar (Settings > Pages > master)

## 2. ARQUITECTURA

- **Patron**: Single File Application. Todo vive en `index.html`: HTML semantico, CSS custom properties (tema oscuro), JavaScript en IIFE con modulo closures.
- **Entry point**: El usuario abre `index.html` en navegador moderno. No hay servidor backend.
- **Flujo principal**:
  1. Arrastra o selecciona un MP3.
  2. jsmediatags lee los metadatos existentes.
  3. El usuario edita campos, agrega/quita portada.
  4. Al guardar:
     - Si formato MP3: cleanAudio() elimina todas las ID3 viejas (inicio, final, ID3v1), browser-id3-writer escribe las nuevas, descarga.
     - Si formato WAV: Web Audio API decodifica, OfflineAudioContext remuestrea/cambia canales, normaliza, encodeWav() genera WAV con LIST/INFO metadata, descarga.
- **Dependencias CDN**:
  - `jsmediatags@3.9.7/dist/jsmediatags.min.js` (lectura tags ID3)
  - `browser-id3-writer@4.4.0/dist/browser-id3-writer.js` (escritura tags ID3)
- **Dependencias nativas**: Web Audio API (decodeAudioData, OfflineAudioContext) — soportada en todos los navegadores modernos.
- **Layout**: Header (titulo/subtitulo) > Main (drop zone > formulario > acciones) > Footer.

## 3. RECURSOS

- **APIs externas**: Ninguna backend. Solo CDN para JS.
- **Claves**: No aplica (no hay API keys, todo es local).
- **Configuracion**: Ningun archivo de configuracion. Todo hardcodeado en el HTML/JS.
- **Esquema de datos (metadatos ID3 editables)**: TIT2 (titulo), TPE1 (artista), TALB (album), TPE2 (artista del album), TYER (anio), TRCK (pista), TCON (genero — implicito via campo), TCOM (compositor), COMM (comentario), APIC (portada tipo 3/front cover).
- **Esquema WAV (LIST INFO)**: INAM (titulo), IART (artista), IPRD (album), ICRD (anio), ITRK (pista), IGNR (genero), ICMT (comentario).
- **Opciones de conversion WAV**:
  - Profundidad de bits: 8, 16, 24, 32 entero, 32 flotante
  - Frecuencia de muestreo: 8000, 11025, 16000, 22050, 32000, 44100, 48000, 88200, 96000, 192000 Hz
  - Canales: mono (1), estereo (2)
  - Normalizar: auto (-1 dB), none (sin normalizar), max (0 dB)

## 4. CAPACIDADES

1. **Leer metadatos MP3**: Carga archivo, muestra titulo/artista/album/anio/pista/genero/compositor/comentario existentes.
2. **Editar metadatos MP3**: Modifica cualquier campo de texto. Solo muestra valores actuales si existen; si no, campos vacios.
3. **Agregar/quitar portada**: Boton "Anadir o arrastrar portada" con drag & drop. Muestra preview y tamano. Boton "Quitar portada". Portada se incrusta como APIC front cover (type 3).
4. **Eliminar imagenes originales**: cleanAudio() elimina todas las ID3v2 (al inicio y al final) e ID3v1. La imagen vieja se elimina por completo; solo queda la nueva si el usuario agrega una.
5. **Guardar MP3 modificado**: Descarga un MP3 con las nuevas tags ID3. Sin portada = sin imagen. Con portada = solo la seleccionada.
6. **Convertir MP3 a WAV**: Decodifica via Web Audio API, remuestrea, cambia canales, normaliza, codifica WAV con metadata LIST/INFO.
7. **Configuracion de conversion**: Permite elegir profundidad de bits, frecuencia de muestreo, canales y normalizacion.
8. **Informacion de tamano**: Muestra tamano original del MP3 y tamano resultante. Para WAV muestra tamano estimado por minuto antes de convertir.
9. **Drag & drop**: Tanto para MP3 (zona principal) como para portada (boton dedicado).

## 5. LECCIONES

1. **browser-id3-writer no acepta File/Blob para APIC**: El `_setPictureFrame` hace `new Uint8Array(t)` donde t es el data. Un File/Blob no es ArrayBuffer; produce array vacio y la portada no se incrusta. **Fix**: Convertir imagen a `ArrayBuffer` via `file.arrayBuffer()` antes de pasar a setFrame. **Verificado**: con ArrayBuffer la portada si se incrusta.

2. **TPE1 y frames multiples esperan arrays**: `browser-id3-writer` requiere que TPE1, TPE2, TCOM y otros frames de multiples valores reciban `[string]` (array), no string plano. Sin array lanza "frame value should be an array of strings". **Fix**: `writer.setFrame('TPE1', [valor])`. **Verificado**: sin array lanza error; con array funciona.

3. **Race condition en portada**: `file.arrayBuffer()` es async. Si el usuario guarda antes de que resuelva, `coverBlob` es null y se guarda sin portada. **Fix**: Variable `coverPending` que guarda la promesa; en submit se hace `await coverPending` antes de construir el writer. **Verificado**: guardado rapido ahora funciona correctamente.

4. **Imagen original persiste sin reset**: Algunos MP3 tienen ID3v2 al inicio y otra al final (o ID3v1 al final). La libreria solo elimina la primera. **Fix**: `cleanAudio()` elimina todas las ID3v2 (loop while al inicio y al final) y el ID3v1. **Verificado**: el archivo limpio no tiene imagen residual.

5. **CSS `input[type="file"] { display: none }` oculta tambien el campo de portada**: La regla global para esconder el file input principal tambien ocultaba el input de portada, haciendo que el usuario no pudiera seleccionar imagen. **Fix**: Boton dedicado `coverBtn` que dispara el input oculto via `click()`, con drag & drop propio. **Verificado**: el boton es visible y funcional.

6. **32-bit int sin clamp produce overflow**: Despues de remuestrear, los samples pueden exceder [-1, 1]. Sin clamp, `Math.round(s * 2147483647)` puede pasar el rango de int32. **Fix**: Clamp explicito para 8, 16, 24 y 32 bits enteros. **Verificado**: archivos extremos no corrompen.

7. **192000 Hz puede fallar en algunos navegadores**: `OfflineAudioContext` con frecuencias muy altas puede lanzar error en navegadores con limitaciones. **Fix**: Mensaje de error sugiriendo 96000 Hz o menor. **No verificado** en todos los navegadores.
