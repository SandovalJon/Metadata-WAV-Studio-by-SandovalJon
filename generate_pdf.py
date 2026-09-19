import os
import re
from fpdf import FPDF
from pypdf import PdfReader

def sanitize(text):
    replacements = {
        '\u2013': '-', '\u2014': '--', '\u2018': "'", '\u2019': "'",
        '\u201c': '"', '\u201d': '"', '\u2026': '...', '\u2022': '-',
        '\u25b6': '>', '\u25cf': '*', '\u2713': '[OK]', '\u2717': '[X]',
        '\u2714': '[OK]', '\u2716': '[X]', '\u2192': '->', '\u2190': '<-',
        '\u2794': '->', '\ud83d': '', '\ude0a': '', '\ude0d': '',
        '\ude09': '', '\ude1f': '', '\ud83c': '', '\ude21': '',
        '\ude0e': '', '\ud83d\ude0a': '', '\ud83d\ude0d': '',
        '\ud83d\ude09': '', '\ud83d\ude1f': '', '\ud83d\ude21': '',
        '\ud83d\ude0e': '', '\ud83d\udc4d': '[OK]', '\ud83d\udc4e': '[X]',
    }
    for k, v in replacements.items():
        text = text.replace(k, v)
    text = re.sub(r'[^\x00-\x7f]+', '', text)
    return text

class PDF(FPDF):
    def header(self):
        self.set_font('Helvetica', 'B', 10)
        self.set_text_color(100, 100, 100)
        self.cell(0, 8, sanitize('Metadata & WAV Studio - Manual'), align='R', new_x='LMARGIN', new_y='NEXT')
        self.line(10, self.get_y(), 200, self.get_y())
        self.ln(4)

    def footer(self):
        self.set_y(-15)
        self.set_font('Helvetica', 'I', 8)
        self.set_text_color(128, 128, 128)
        self.cell(0, 10, f'Pagina {self.page_no()}/{{nb}}', align='C')

    def chapter_title(self, title):
        self.set_font('Helvetica', 'B', 14)
        self.set_text_color(30, 30, 30)
        self.cell(0, 10, sanitize(title), new_x='LMARGIN', new_y='NEXT')
        self.ln(2)

    def section_title(self, title):
        self.set_font('Helvetica', 'B', 11)
        self.set_text_color(60, 60, 60)
        self.cell(0, 8, sanitize(title), new_x='LMARGIN', new_y='NEXT')
        self.ln(1)

    def body_text(self, text):
        self.set_font('Helvetica', '', 10)
        self.set_text_color(30, 30, 30)
        self.multi_cell(0, 6, sanitize(text))
        self.ln(1)

    def bullet(self, text):
        self.set_font('Helvetica', '', 10)
        self.set_text_color(30, 30, 30)
        x = self.get_x()
        self.cell(8, 6, '-')
        self.multi_cell(0, 6, sanitize(text), new_x='LMARGIN')
        self.ln(0.5)

    def table_row(self, col1, col2, bold=False):
        self.set_font('Helvetica', 'B' if bold else '', 10)
        self.set_text_color(30, 30, 30)
        w1 = 55
        w2 = 125
        self.cell(w1, 7, sanitize(col1), border=1)
        self.cell(w2, 7, sanitize(col2), border=1, new_x='LMARGIN', new_y='NEXT')

pdf = PDF()
pdf.alias_nb_pages()
pdf.set_auto_page_break(auto=True, margin=20)
pdf.add_page()

sections = {
    'Ficha': lambda: (
        pdf.table_row('Campo', 'Valor', bold=True),
        pdf.table_row('Nombre', 'Metadata & WAV Studio'),
        pdf.table_row('Tipo', 'Pagina web client-side (single-file)'),
        pdf.table_row('Archivo', 'index.html'),
        pdf.table_row('Stack', 'HTML + CSS + JS vanilla, jsmediatags, browser-id3-writer, Web Audio API'),
        pdf.table_row('Repo', 'https://github.com/SandovalJon/Metadata.git'),
        pdf.table_row('Branch', 'master'),
        pdf.table_row('Version', 'v1 (2026-09-19)'),
        pdf.ln(4),
    ),
    'Arquitectura y flujo': lambda: (
        pdf.body_text('Un solo archivo index.html (aprox. 830 lineas, 27 KB). Tema oscuro con CSS custom properties. IIFE en JS para encapsular estado.'),
        pdf.body_text('Flujo: el usuario carga un MP3, edita metadatos, elige formato de salida (MP3 o WAV), configura opciones, descarga el resultado.'),
        pdf.body_text('Las dependencias se cargan desde CDN al abrir la pagina (no hay build, no hay servidor).'),
        pdf.body_text('La conversion WAV usa OfflineAudioContext para remuestrear y cambiar canales; el encoder WAV esta implementado en vanilla JS.'),
        pdf.ln(2),
    ),
    'Capacidades': lambda: (
        pdf.bullet('Leer metadatos MP3 - titulo, artista, album, artista del album, anio, pista, genero, compositor, comentario, portada existente.'),
        pdf.bullet('Editar metadatos MP3 - todos los campos de texto editables.'),
        pdf.bullet('Portada - agregar/quitar con drag & drop o selector de archivos.'),
        pdf.bullet('Eliminar imagenes viejas - cleanAudio() elimina todas las ID3 e ID3v1 antes de escribir.'),
        pdf.bullet('Guardar MP3 - descarga el archivo con las nuevas tags ID3.'),
        pdf.bullet('Convertir MP3 a WAV - decodifica, remuestrea, cambia canales, normaliza, codifica WAV con metadata LIST/INFO.'),
        pdf.bullet('Configuracion de conversion - bits (8/16/24/32int/32float), frecuencia (8k-192k Hz), canales (mono/estereo), normalizacion (auto/none/max).'),
        pdf.bullet('Tamano - muestra tamano original vs resultado; para WAV muestra estimado por minuto.'),
        pdf.ln(2),
    ),
    'APIs, claves y recursos': lambda: (
        pdf.bullet('jsmediatags@3.9.7 - CDN: cdn.jsdelivr.net/npm/jsmediatags@3.9.7/dist/jsmediatags.min.js - lectura de tags ID3.'),
        pdf.bullet('browser-id3-writer@4.4.0 - CDN: cdn.jsdelivr.net/npm/browser-id3-writer@4.4.0/dist/browser-id3-writer.js - escritura de tags ID3. Solo acepta ArrayBuffer. Frames multiples requieren array de strings.'),
        pdf.bullet('Web Audio API - nativa del navegador. decodeAudioData + OfflineAudioContext.'),
        pdf.bullet('No hay claves ni endpoints. Todo es local y offline.'),
        pdf.ln(2),
    ),
    'Datos y memoria': lambda: (
        pdf.body_text('No hay base de datos, localStorage ni estado persistente. Todo es ephemeral.'),
        pdf.body_text('Tags ID3 editables: TIT2, TPE1, TALB, TPE2, TYER, TRCK, TCON, TCOM, COMM, APIC.'),
        pdf.body_text('Tags WAV (LIST INFO): INAM, IART, IPRD, ICRD, ITRK, IGNR, ICMT.'),
        pdf.body_text('Variables de estado JS: currentFile, originalTags, coverBlob, coverPending, originalSize.'),
        pdf.ln(2),
    ),
    'Despliegue y operacion': lambda: (
        pdf.bullet('Local: Abrir index.html en navegador. Requiere CDN la primera vez.'),
        pdf.bullet('GitHub Pages: Settings > Pages > Source: master.'),
        pdf.bullet('No hay build ni servidor. No hay npm, no hay deploy script.'),
        pdf.bullet('Git: git add . && git commit -m "mensaje" && git push origin master.'),
        pdf.ln(2),
    ),
    'Skills y lecciones': lambda: (
        pdf.bullet('ID3Writer y ArrayBuffer - browser-id3-writer solo acepta ArrayBuffer. Siempre convertir con file.arrayBuffer().'),
        pdf.bullet('Frames multiples - TPE1, TPE2, TCOM requieren array: [valor], no valor.'),
        pdf.bullet('Race condition - coverPending debe resolverse antes del guardado. Usar await coverPending.'),
        pdf.bullet('Limpieza de tags - cleanAudio() elimina todas las ID3 (inicio + final) e ID3v1.'),
        pdf.bullet('CSS file input - input[type="file"] display:none oculta todos los file inputs. Usar boton dedicado.'),
        pdf.bullet('Clamp en int - Siempre clampear samples antes de escribir a PCM int para evitar overflow.'),
        pdf.bullet('Frecuencias altas - 192k puede fallar en algunos navegadores. Ofrecer fallback a 96k.'),
        pdf.ln(2),
    ),
    'Estado y pendientes': lambda: (
        pdf.body_text('Version actual: v1 (2026-09-19, commit 527d11a).'),
        pdf.body_text('Funcionalidad completa: Editor de metadatos + convertidor WAV funcional.'),
        pdf.body_text('Pendientes (ideas):'),
        pdf.bullet('Soporte para mas formatos de entrada (M4A, FLAC, OGG).'),
        pdf.bullet('Soporte para metadatos en WAV de salida (actual: LIST/INFO basico).'),
        pdf.bullet('Soporte para portada en archivos FLAC/OGG.'),
        pdf.bullet('Editor de waveform visual.'),
        pdf.bullet('Soporte para lotes (varios archivos a la vez).'),
        pdf.bullet('Dithering configurable para 16/8 bits.'),
        pdf.ln(2),
    ),
}

for title, render_fn in sections.items():
    pdf.chapter_title(title)
    render_fn()

pdf_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'Metadata-Manual-Skills.pdf')
pdf.output(pdf_path)
print(f'PDF generado: {pdf_path}')

reader = PdfReader(pdf_path)
print(f'Paginas: {len(reader.pages)}')

sections_found = []
all_text = ''
for page in reader.pages:
    all_text += page.extract_text() or ''

expected = ['Ficha', 'Arquitectura', 'Capacidades', 'APIs', 'Datos', 'Despliegue', 'Skills', 'Estado']
for s in expected:
    found = s.lower() in all_text.lower()
    sections_found.append(f'{s}: {"[OK]" if found else "[FALTA]"}')
    print(f'  Seccion {s}: {"OK" if found else "FALTA"}')

print('Verificacion completa.')
