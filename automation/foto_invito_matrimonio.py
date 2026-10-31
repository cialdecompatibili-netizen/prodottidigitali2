# -*- coding: utf-8 -*-
"""
Foto prodotto 'invito-matrimonio' in IT e EN, disegnata con Pillow (testo VERO, nella lingua giusta).
Perche' non Gemini: sbaglia date/lettere e scrive sempre in inglese (vedi CLAUDE.md, immagini multilingua).
Uso: python automation/foto_invito_matrimonio.py
Scrive: assets/images/prodotti/invito-matrimonio.webp (IT) e invito-matrimonio-en.webp (EN).
Il test del calendario: 12 giugno 2027 e' un sabato (1 gennaio 2027 = venerdi').
Font: Georgia + Segoe Script di Windows (C:\\Windows\\Fonts).
"""
import math, os
from PIL import Image, ImageDraw, ImageFont, ImageFilter

S = 2000  # si disegna a 2000 px e si riduce a 1000 (bordi piu' lisci)
RADICE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(RADICE, 'assets', 'images', 'prodotti')
FD = r'C:\Windows\Fonts'

PAPER = (250, 246, 238); INK = (63, 90, 69); SAGE = (125, 148, 117)
GOLD = (184, 154, 90); RULE = (214, 220, 208); DARK = (84, 112, 88); LIGHT = (164, 184, 154)

def F(n, s): return ImageFont.truetype(os.path.join(FD, n), s)

TESTI = {
 'it': dict(inv1='CON GIOIA VI INVITIAMO', inv2='AL NOSTRO MATRIMONIO', n1='Giulia', n2='Marco',
            data='Sabato 12 giugno 2027', ora='alle ore 16:00', luogo='Villa dei Cipressi', reg='TOSCANA',
            conf='Conferma entro il 12 maggio', menu='Menù',
            portate=['ANTIPASTO', 'PRIMO', 'SECONDO', 'DOLCE'], risp='Risposta', nome='Nome e cognome',
            si='Parteciperò con gioia', no='Non potrò partecipare', entro='Entro il 12 maggio', ospite='Anna Rossi'),
 'en': dict(inv1='TOGETHER WITH OUR FAMILIES', inv2='WE INVITE YOU TO OUR WEDDING', n1='Julia', n2='Mark',
            data='Saturday, June 12, 2027', ora='at 4:00 PM', luogo='Cypress Grove Estate', reg='TUSCANY',
            conf='Kindly reply by May 12', menu='Menu',
            portate=['STARTER', 'FIRST COURSE', 'MAIN COURSE', 'DESSERT'], risp='RSVP', nome='Full name',
            si='Joyfully accept', no='Regretfully decline', entro='Reply by May 12', ospite='Anna Smith'),
}

def tw(d, t, f, sp=0):
    return d.textlength(t, font=f) if sp == 0 else sum(d.textlength(c, font=f) for c in t) + sp * (len(t) - 1)

def ctext(d, cx, y, t, f, fill, sp=0):
    x = cx - tw(d, t, f, sp) / 2
    if sp == 0:
        d.text((x, y), t, font=f, fill=fill); return
    for c in t:
        d.text((x, y), c, font=f, fill=fill); x += d.textlength(c, font=f) + sp

def carta(w, h, fill=PAPER):
    im = Image.new('RGBA', (w, h), fill + (255,))
    d = ImageDraw.Draw(im)
    return im, d

def cornice(d, w, h, m=40):
    d.rectangle([m, m, w - m, h - m], outline=GOLD, width=3)
    d.rectangle([m + 16, m + 16, w - m - 16, h - m - 16], outline=GOLD, width=1)

def rombo(d, cx, cy, r, col):
    d.polygon([(cx, cy - r), (cx + r, cy), (cx, cy + r), (cx - r, cy)], fill=col)

def divisore(d, cx, y, w=220):
    d.line([cx - w // 2, y, cx - 18, y], fill=GOLD, width=3)
    d.line([cx + 18, y, cx + w // 2, y], fill=GOLD, width=3)
    rombo(d, cx, y, 9, GOLD)

def invito(t):
    w, h = 860, 1200
    im, d = carta(w, h); cornice(d, w, h); c = w // 2
    f_s = F('georgia.ttf', 26)
    ctext(d, c, 150, t['inv1'], f_s, SAGE, 4); ctext(d, c, 196, t['inv2'], f_s, SAGE, 4)
    sc = F('segoesc.ttf', 120)
    ctext(d, c, 290, t['n1'], sc, INK)
    ctext(d, c, 430, '&', F('segoesc.ttf', 84), GOLD)
    ctext(d, c, 520, t['n2'], sc, INK)
    divisore(d, c, 740)
    ctext(d, c, 790, t['data'], F('georgiai.ttf', 46), INK)
    ctext(d, c, 862, t['ora'], F('georgia.ttf', 34), DARK)
    ctext(d, c, 940, t['luogo'], F('georgiab.ttf', 40), INK)
    ctext(d, c, 1000, t['reg'], F('georgia.ttf', 24), SAGE, 6)
    ctext(d, c, 1080, t['conf'], F('georgiai.ttf', 28), DARK)
    return im

def menu(t):
    w, h = 520, 1200
    im, d = carta(w, h); cornice(d, w, h, 36); c = w // 2
    ctext(d, c, 110, t['menu'], F('segoesc.ttf', 96), INK)
    divisore(d, c, 262, 180)
    y = 330
    for p in t['portate']:
        ctext(d, c, y, p, F('georgia.ttf', 26), SAGE, 5)
        d.line([c - 150, y + 78, c + 150, y + 78], fill=RULE, width=3)
        d.line([c - 110, y + 118, c + 110, y + 118], fill=RULE, width=3)
        y += 200
    return im

def risposta(t):
    w, h = 760, 520
    im, d = carta(w, h); cornice(d, w, h, 28)
    ctext(d, w // 2, 52, t['risp'], F('segoesc.ttf', 74), INK)
    d.text((90, 168), t['nome'], font=F('georgia.ttf', 28), fill=SAGE)
    d.line([90, 228, w - 90, 228], fill=RULE, width=3)
    f = F('georgia.ttf', 32)
    for i, k in enumerate(('si', 'no')):
        y = 280 + i * 70
        d.rectangle([90, y + 4, 122, y + 36], outline=GOLD, width=3)
        d.text((146, y), t[k], font=f, fill=INK)
    ctext(d, w // 2, 432, t['entro'], F('georgiai.ttf', 26), DARK)
    return im

def segnaposto(t):
    w, h = 520, 260
    im, d = carta(w, h)
    d.rectangle([0, 176, w, h], fill=(240, 234, 222))
    d.line([0, 176, w, 176], fill=GOLD, width=3)
    d.rectangle([0, 0, w - 1, h - 1], outline=RULE, width=2)
    ctext(d, w // 2, 40, t['ospite'], F('segoesc.ttf', 66), INK)
    divisore(d, w // 2, 148, 140)
    return im

def metti(base, carta_im, cx, cy, ang):
    r = carta_im.rotate(ang, resample=Image.BICUBIC, expand=True)
    pad = 90
    ombra = Image.new('RGBA', (r.width + 2 * pad, r.height + 2 * pad), (0, 0, 0, 0))
    sh = Image.new('RGBA', r.size, (45, 58, 45, 255)); sh.putalpha(r.split()[3].point(lambda a: int(a * 0.30)))
    ombra.paste(sh, (pad, pad + 26)); ombra = ombra.filter(ImageFilter.GaussianBlur(26))
    x, y = int(cx - r.width / 2), int(cy - r.height / 2)
    base.paste(ombra, (x - pad, y - pad), ombra)
    base.paste(r, (x, y), r)

def foglia(d, x, y, ang, L, W, col):
    n = 24; top = []; bot = []
    for i in range(n + 1):
        t = i / n; py = W * math.sin(math.pi * t) * 0.5
        top.append((L * t, py)); bot.append((L * t, -py))
    pts = top + bot[::-1]; ca, sa = math.cos(ang), math.sin(ang)
    d.polygon([(x + px * ca - py * sa, y + px * sa + py * ca) for px, py in pts], fill=col)

def ramo(layer, x0, y0, ang_deg, length, bend, flip=1):
    d = ImageDraw.Draw(layer); a = math.radians(ang_deg)
    dx, dy = math.cos(a), math.sin(a); nx, ny = -dy, dx; steps = 40; pts = []
    for i in range(steps + 1):
        t = i / steps; off = bend * math.sin(math.pi * t) * flip
        pts.append((x0 + dx * length * t + nx * off, y0 + dy * length * t + ny * off))
    d.line(pts, fill=DARK, width=7, joint='curve')
    cols = (SAGE, LIGHT, DARK); k = 0
    for i in range(4, steps, 3):
        px, py = pts[i]; qx, qy = pts[i + 1]; ta = math.atan2(qy - py, qx - px)
        s = 1 - (i / steps) * 0.55; lato = 1 if k % 2 == 0 else -1
        foglia(d, px, py, ta + lato * math.radians(42), 150 * s, 62 * s, cols[k % 3]); k += 1
    ex, ey = pts[-1]; px, py = pts[-2]
    foglia(d, ex, ey, math.atan2(ey - py, ex - px), 90, 40, SAGE)

def crea(lang):
    t = TESTI[lang]
    base = Image.new('RGB', (S, S), (255, 255, 255))
    metti(base, menu(t), 1390, 800, 4)
    metti(base, invito(t), 680, 960, -3)
    metti(base, risposta(t), 1420, 1490, 2)
    metti(base, segnaposto(t), 560, 1660, -2)
    layer = Image.new('RGBA', (S, S), (0, 0, 0, 0))
    ramo(layer, 270, 300, 35, 215, 36)
    ramo(layer, 1850, 1790, -145, 300, 45, -1)
    base.paste(layer, (0, 0), layer)
    return base.resize((1000, 1000), Image.LANCZOS)

if __name__ == '__main__':
    os.makedirs(OUT, exist_ok=True)
    for lang, nome in (('it', 'invito-matrimonio.webp'), ('en', 'invito-matrimonio-en.webp')):
        p = os.path.join(OUT, nome); crea(lang).save(p, 'WEBP', quality=86)
        print('OK', p, os.path.getsize(p) // 1024, 'KB')
