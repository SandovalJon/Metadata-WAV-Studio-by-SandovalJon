# Audio Studio — Manual de Skills

## 1. Ficha

- **Nombre**: Audio Studio
- **Tipo**: PWA ( Progressive Web App)
- **Función**: Editor de metadatos de audio, conversor MP3/WAV, gestor de portadas
- **Versión**: v2.0.0
- **URL**: https://sandovaljon.github.io/Metadata-WAV-Studio-by-SandovalJon/
- **Repo**: https://github.com/SandovalJon/Metadata-WAV-Studio-by-SandovalJon

## 2. Arquitectura y flujo

### Stack
- HTML5 + CSS3 + JavaScript vanilla (sin frameworks)
- Firebase (autenticación + Firestore)
- Service Worker (offline)

### Archivos
| Archivo | Función |
|---------|---------|
| index.html | App completa (HTML + CSS + JS) |
| sw.js | Service Worker para offline |
| manifest.json | Configuración PWA |
| icon-192.png | Icono 192x192 |
| icon-512.png | Icono 512x512 |

### Flujo de uso
1. Arrastrar o seleccionar archivo MP3/WAV
2. Editar metadatos en pestaña "Editar"
3. Configurar conversión en pestaña "Convertir"
4. Guardar y descargar

## 3. Capacidades

### Editor de metadatos
- Campos: título, artista, álbum, artista del álbum, año, pista, género, compositor, comentario
- Portada: agregar/quitar imagen JPG/PNG
- Soporta MP3 (ID3v2) y WAV (LIST-INFO)
- Procesamiento por lotes (múltiples archivos)

### Conversión de audio
- MP3 → WAV (configurable)
- WAV → MP3 (192kbps, estéreo, 44100Hz)
- WAV → WAV (re-guardar con metadatos)

### Configuración WAV
- Profundidad de bits: 8, 16, 24, 32, 32 float
- Frecuencia: 8000 a 192000 Hz
- Canales: Mono/Estéreo
- Normalizar: Ninguno, Automático (-1dB), Máximo (0dB)
- Dithering: Ninguno, TPDF, High Pass
- Resampleo: Baja, Media, Alta

### Presets
- Guardar configuración con nombre
- Cargar preset existente
- Resetear a valores mínimos
- Eliminar preset

### PWA
- Instalable en celular (Agregar a pantalla de inicio)
- Offline después de primera carga
- Service Worker con caché de librerías

## 4. APIs, claves y recursos

### Firebase
- Proyecto: metadata---wav-studio
- Auth: Google Sign-In
- Firestore: datos de usuario

### Librerías CDN
- jsmediatags@3.9.7 (lectura ID3)
- browser-id3-writer@4.4.0 (escritura ID3)
- lamejs@1.2.1 (codificación MP3)
- Firebase 10.12.2 (auth + firestore)

### localStorage
| Key | Uso |
|-----|-----|
| theme | Tema seleccionado |
| lastTab | Última pestaña |
| wavPresets | Presets de conversión |
| draftFields | Borrador de campos |
| compactMode | Modo compacto |
| windowSize | Tamaño de ventana |

## 5. Datos y memoria

### Tags ID3 (MP3)
| Tag | Campo |
|-----|-------|
| TIT2 | Título |
| TPE1 | Artista |
| TALB | Álbum |
| TPE2 | Artista del álbum |
| TYER | Año |
| TRCK | Pista |
| TCON | Género |
| TCOM | Compositor |
| COMM | Comentario |
| APIC | Portada |

### LIST-INFO (WAV)
| Chunk | Campo |
|-------|-------|
| INAM | Título |
| IART | Artista |
| IPRD | Álbum |
| ICRD | Año |
| ITRK | Pista |
| IGNR | Género |
| ICMT | Comentario |

## 6. Despliegue y operación

### Comandos
```bash
# Commit y push a master
git add -A && git commit -m "Mensaje" && git push origin master

# Deploy a GitHub Pages
git checkout gh-pages && git merge master && git push origin gh-pages && git checkout master
```

### Service Worker
- Caché: audio-studio-v2
- Para actualizar: cambiar nombre del caché (v2 → v3)
- Offline: funciona después de primera carga

### Actualizaciones
- Automático: banner "Nueva versión disponible"
- Manual: botón 🔄 en el header
- Forzado: Ctrl+Shift+R o borrar datos del sitio

## 7. Skills y lecciones

### Skills del proyecto
- Edición de metadatos ID3/LIST-INFO
- Conversión de audio (Web Audio API + OfflineAudioContext)
- Codificación MP3 (lamejs)
- PWA con Service Worker
- Firebase Auth + Firestore
- Diseño fluido con clamp()
- Toast notifications
- Skeleton loading

### Lecciones aprendidas
1. `display:none` no funciona en `<option>` — usar remove/add dinámico
2. Service Worker cachea versiones — cambiar nombre del caché para invalidar
3. `flex:1` en button CSS global afecta todos — sobreescribir con `flex:0 0 auto`
4. GitHub Pages subdirectorio — usar rutas absolutas con el path completo
5. Dithering TPDF es estándar para música
6. Plataformas comprimen audio — 24bit/48kHz es óptimo

## 8. Estado y pendientes

### Versión actual: v2.0.0 (2026-09-23)

### Pendientes (ideas, no compromisos)
- Undo/redo global (no solo por campo)
- Modo oscuro automático según sistema
- Exportar configuración JSON
- Copiar metadatos al portapapeles
- Efecto ripple en botones
- Partículas de fondo
- Barra de progreso animada en header
- Navegación con flechas del teclado
- Buscar en lista de idiomas
- Modo compacto
- Animación de carga al abrir archivo
- Recordar tamaño de ventana
- Scroll to top al cambiar de pestaña
