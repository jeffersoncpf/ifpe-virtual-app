# Gera os assets de marca do app IFPE Virtual a partir do símbolo IF (vetor).
import os, sys
OUT = sys.argv[1]
GREEN = "#2F9E41"   # verde usado pelo AVEA (--primary)
SYMG  = "#349A46"   # verde do símbolo IF no logo do AVEA
RED   = "#CA2027"   # vermelho do símbolo IF
# grade 3 colunas x 4 linhas, célula 100, quadrado 88, cantos 10
CELLS = [(0,0,'c'),(1,0,'s'),(2,0,'s'),(0,1,'s'),(1,1,'s'),(0,2,'s'),(1,2,'s'),(2,2,'s'),(0,3,'s'),(1,3,'s')]
S, STEP, R = 88, 100, 10
W, H = 2*STEP+S, 3*STEP+S   # 288 x 388
def symbol(x, y, scale, mono=None):
    g = [f'<g transform="translate({x},{y}) scale({scale})">']
    for c, r, k in CELLS:
        if k == 'c':
            g.append(f'<circle cx="{c*STEP+S/2}" cy="{r*STEP+S/2}" r="{S/2}" fill="{mono or RED}"/>')
        else:
            g.append(f'<rect x="{c*STEP}" y="{r*STEP}" width="{S}" height="{S}" rx="{R}" fill="{mono or SYMG}"/>')
    g.append('</g>'); return ''.join(g)
def svg(w, h, body, bg=None):
    b = f'<rect width="{w}" height="{h}" fill="{bg}"/>' if bg else ''
    return f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}">{b}{body}</svg>'
def centered(w, h, sym_h, bg=None, mono=None, dy=0):
    sc = sym_h / H; sw = W*sc
    return svg(w, h, symbol((w-sw)/2, (h-sym_h)/2+dy, sc, mono), bg)
FONT = "font-family:Inter,Arial,sans-serif"
def wordmark(w, h, dark=False):
    sc = (h*0.86)/H; sw = W*sc; tx = sw + h*0.22
    c1 = "#FFFFFF" if dark else "#1F2A22"; c2 = "#E6F4E8" if dark else GREEN
    body = symbol(0, h*0.07, sc) + \
      f'<text x="{tx}" y="{h*0.50}" style="{FONT};font-weight:800;font-size:{h*0.36}px" fill="{c1}">IFPE <tspan fill="{c2}">Virtual</tspan></text>' + \
      f'<text x="{tx}" y="{h*0.80}" style="{FONT};font-weight:500;font-size:{h*0.135}px" fill="{c1}">Ambiente Virtual de Ensino e Aprendizagem</text>'
    return svg(w, h, body)
files = {
  'icon.svg':            centered(1024, 1024, 600, bg="#FFFFFF"),
  'icon-foreground.svg': centered(1024, 1024, 430),
  'smallicon.svg':       centered(96, 96, 86, mono="#FFFFFF"),
  'splash.svg':          centered(2732, 2732, 520, bg="#FFFFFF"),
  'logo.svg':            wordmark(1200, 294),
  'symbol.svg':          svg(W, H, symbol(0, 0, 1)),
}
os.makedirs(OUT, exist_ok=True)
for n, s in files.items():
    open(os.path.join(OUT, n), 'w').write(s)
# Vetor Android (splash animado): ícone de 288dp centrado num viewport 432 (área segura do Android 12+)
V = 432; sc = 0.42; ox = (V - W*sc)/2; oy = (V - H*sc)/2
paths = []
for c, r, k in CELLS:
    x0, y0 = ox + c*STEP*sc, oy + r*STEP*sc; s = S*sc
    if k == 'c':
        rr = s/2; cx = x0+rr; cy = y0+rr
        d = f"M{cx-rr:.2f},{cy:.2f}a{rr:.2f},{rr:.2f} 0,1 1,{2*rr:.2f},0a{rr:.2f},{rr:.2f} 0,1 1,{-2*rr:.2f},0Z"; col = RED
    else:
        q = R*sc
        d = (f"M{x0+q:.2f},{y0:.2f}h{s-2*q:.2f}a{q:.2f},{q:.2f} 0,0 1,{q:.2f},{q:.2f}v{s-2*q:.2f}"
             f"a{q:.2f},{q:.2f} 0,0 1,{-q:.2f},{q:.2f}h{-(s-2*q):.2f}a{q:.2f},{q:.2f} 0,0 1,{-q:.2f},{-q:.2f}"
             f"v{-(s-2*q):.2f}a{q:.2f},{q:.2f} 0,0 1,{q:.2f},{-q:.2f}Z"); col = SYMG
    paths.append(f'  <path android:pathData="{d}" android:fillColor="{col}" />')
open(os.path.join(OUT, 'android-splash.xml'), 'w').write(
  '<vector xmlns:android="http://schemas.android.com/apk/res/android"\n'
  f'    android:width="{V}dp" android:height="{V}dp"\n    android:viewportWidth="{V}" android:viewportHeight="{V}">\n' + '\n'.join(paths) + '\n</vector>\n')
