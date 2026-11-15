"""Encaixa capturas reais e pares responsivos sem JavaScript no cliente."""
import argparse
import html
import json
from pathlib import Path
import re
import struct

ROOT = Path(__file__).resolve().parents[1]

def capture(slot, root, eager=False, paired=False):
    name = slot['file']
    if Path(name).name != name or not name.endswith('.png'):
        raise ValueError('Nome de captura inválido')
    data = (root / 'assets/prints' / name).read_bytes()
    if len(data) < 24 or data[:8] != b'\x89PNG\r\n\x1a\n' or data[12:16] != b'IHDR':
        raise ValueError('PNG inválido: ' + name)
    width, height = struct.unpack('>II', data[16:24])
    if width < 100 or height < 100:
        raise ValueError('Captura pequena demais: ' + name)
    title = html.escape(slot['title'], quote=True)
    device = slot.get('device', 'phone')
    stem = Path(name).stem
    large = min(1440, width)
    sizes = '(max-width: 640px) 65vw, 210px' if device == 'phone' else '(max-width: 640px) 1px, (max-width: 1024px) 30vw, 420px'
    if device == 'laptop' and not paired:
        sizes = '(max-width: 640px) 85vw, (max-width: 1024px) 40vw, 520px'
    priority = 'loading="eager" fetchpriority="high"' if eager else 'loading="lazy"'
    image = f'<img class="product-print" src="assets/prints/{stem}-720.webp" srcset="assets/prints/{stem}-720.webp 720w, assets/prints/{stem}-{large}.webp {large}w" sizes="{sizes}" alt="Captura real do Tilevu: {title}" width="{width}" height="{height}" {priority} decoding="async">'
    # Only paired desktops hidden below 640 px use a tiny source, including the hero.
    if device == 'laptop' and paired:
        image = f'<picture><source media="(max-width: 640px)" srcset="assets/blank.svg">{image}</picture>'
    bar = '<div class="device-bar" aria-hidden="true"><i></i><i></i><i></i><span>Tilevu</span></div>'
    return f'<figure class="device {device}" data-print="{name}">{bar}<a href="assets/prints/{name}" aria-label="Ampliar captura: {title}">{image}</a><figcaption>{title}</figcaption></figure>'

def render(content, root=ROOT, require_all=False):
    slots = json.loads((root / 'assets/prints/manifest.json').read_text(encoding='utf-8'))
    missing = []
    for slot in slots:
        key = slot.get('id', slot['file'])
        pattern = re.compile(r'(<!-- print:' + re.escape(key) + r':start -->)(.*?)(<!-- print:' + re.escape(key) + r':end -->)', re.S)
        found = pattern.search(content)
        if not found:
            raise ValueError('Slot ausente: ' + key)
        members = [slot] + ([slot['companion']] if slot.get('companion') else [])
        absent = []
        for item in members:
            name = item['file']
            if Path(name).name != name or not name.endswith('.png'):
                raise ValueError('Nome de captura inválido')
            if not (root / 'assets/prints' / name).exists():
                absent.append(name)
        if absent:
            missing.extend(absent)
            if 'class="product-print"' in found.group(2):
                raise ValueError('Captura anteriormente integrada foi removida: ' + key)
            continue
        body = ''.join(capture(item, root, slot.get('eager', False), paired=bool(slot.get('companion'))) for item in members)
        if slot.get('companion'):
            body = f'<div class="device-pair">{body}</div>'
        content = pattern.sub(lambda m: m.group(1) + body + m.group(3), content)
    if missing and require_all:
        raise ValueError('Capturas reais pendentes: ' + ', '.join(missing))
    return content, missing

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--require-all', action='store_true')
    args = parser.parse_args()
    page = ROOT / 'index.html'
    try:
        result, missing = render(page.read_text(encoding='utf-8'), require_all=args.require_all)
    except ValueError as error:
        parser.exit(1, str(error) + '\n')
    page.write_text(result, encoding='utf-8')
    print(f'Capturas pendentes: {len(missing)}')

if __name__ == '__main__':
    main()
