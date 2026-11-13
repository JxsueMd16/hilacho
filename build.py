# Genera index.html (lo que se publica) a partir de src/index.html.
# Solo hace cambios de texto seguros; el código fuente queda legible en src/.
#  1. quita comentarios de línea completa, sangrías y líneas vacías
#  2. acorta patrones repetidos con alias definidos al inicio del <script>
#  3. une líneas cuando la línea anterior termina en ; { , ( (no cambia el significado)
import sys, os, re
os.chdir(os.path.dirname(os.path.abspath(__file__)))
s = open('src/index.html', encoding='utf-8').read()

lineas = [l.strip() for l in s.split('\n')]
lineas = [l for l in lineas if l and not l.startswith('//')]
s = '\n'.join(lineas)

ALIAS = 'let MA=Math,BP=()=>x.beginPath(),FL=()=>x.fill(),SK=()=>x.stroke(),SV=()=>x.save(),RS=()=>x.restore(),LT=(a,b)=>x.lineTo(a,b),MT=(a,b)=>x.moveTo(a,b),FR=(a,b,c,d)=>x.fillRect(a,b,c,d),TR=(a,b)=>x.translate(a,b),AR=(a,b,c,d,e)=>x.arc(a,b,c,d,e);'
for nombre in ['MA', 'BP', 'FL', 'SK', 'SV', 'RS', 'LT', 'MT', 'FR', 'TR', 'AR']:
    assert not re.search(r'\b' + nombre + r'\b', s), 'el alias ya existe en el código: ' + nombre
for a, b in [('Math.', 'MA.'), ('x.beginPath()', 'BP()'), ('x.fill()', 'FL()'),
             ('x.stroke()', 'SK()'), ('x.save()', 'SV()'), ('x.restore()', 'RS()'),
             ('x.lineTo(', 'LT('), ('x.moveTo(', 'MT('), ('x.fillRect(', 'FR('), ('x.translate(', 'TR('), ('x.arc(', 'AR('),
             ('const ', 'let ')]:
    s = s.replace(a, b)
# renombra identificadores largos que solo aparecen como variables/funciones
RENOMBRES = ['nivel', 'tinta', 'ovillo', 'shake', 'parts', 'dedos', 'finTrazo', 'gatoEn', 'reaparecer', 'dibEnem', 'subrayado', 'sobreHilo']
for i, w in enumerate(RENOMBRES):
    nuevo = 'Z' + chr(65 + i)
    assert not re.search(r'\b' + nuevo + r'\b', s), 'nombre ocupado: ' + nuevo
    assert not re.search(r'\.' + w + r'\b', s), 'se usa como propiedad: ' + w
    s = re.sub(r'\b' + w + r'\b', nuevo, s)
s = s.replace('<script>\n', '<script>\n' + ALIAS + '\n', 1)

out, lineas = [], s.split('\n')
for l in lineas:
    if out and out[-1][-1] in ';{,(':
        out[-1] += l
    else:
        out.append(l)
m = '\n'.join(out) + '\n'

open('index.html', 'w', encoding='utf-8').write(m)
n = len(m.encode('utf-8'))
print(f'index.html: {n} bytes ({n/1024:.1f} KiB) de 32 KB')
sys.exit(1 if n > 32000 else 0)
