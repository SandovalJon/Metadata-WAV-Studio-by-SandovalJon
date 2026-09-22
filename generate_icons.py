#!/usr/bin/env python3
import struct, zlib

def create_png(size, bg=(13,17,23), accent=(88,166,255)):
    rows = []
    for y in range(size):
        row = b'\x00'
        for x in range(size):
            cx, cy = size//2, size//2
            dx, dy = x - cx, y - cy
            dist = (dx*dx + dy*dy) ** 0.5
            r = size * 0.42
            if dist < r * 0.35:
                c = (88, 200, 255)
            elif dist < r * 0.7:
                c = (88, 166, 255)
            elif dist < r:
                t = (dist - r*0.7) / (r*0.3)
                c = tuple(int(accent[i]*(1-t) + bg[i]*t) for i in range(3))
            else:
                c = bg
            row += bytes(c)
        rows.append(row)
    
    def chunk(ctype, data):
        c = ctype + data
        return struct.pack('>I', len(data)) + c + struct.pack('>I', zlib.crc32(c) & 0xffffffff)
    
    ihdr = struct.pack('>IIBBBBB', size, size, 8, 2, 0, 0, 0)
    raw = b''.join(rows)
    idat = zlib.compress(raw)
    
    return b'\x89PNG\r\n\x1a\n' + chunk(b'IHDR', ihdr) + chunk(b'IDAT', idat) + chunk(b'IEND', b'')

with open('icon-192.png', 'wb') as f:
    f.write(create_png(192))
with open('icon-512.png', 'wb') as f:
    f.write(create_png(512))
print('Icons created')
