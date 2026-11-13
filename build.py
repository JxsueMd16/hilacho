# Genera index.html (lo que se publica) a partir de src/index.html:
# quita comentarios de línea completa, sangrías y líneas vacías. No cambia el código.
import re,sys
s=open('src/index.html',encoding='utf-8').read()
out=[]
for l in s.split('\n'):
    t=l.strip()
    if not t or t.startswith('//'):continue
    out.append(t)
m='\n'.join(out)+'\n'
open('index.html','w',encoding='utf-8').write(m)
n=len(m.encode('utf-8'))
print(f'index.html: {n} bytes ({n/1024:.1f} KiB) de 32 KB')
sys.exit(1 if n>32000 else 0)
