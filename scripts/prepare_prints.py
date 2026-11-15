"""Encaixa capturas reais sem JS no cliente e sem criar telas artificiais."""
import argparse
import html
import json
from pathlib import Path
import re
import struct

ROOT = Path(__file__).resolve().parents[1]

def render(content, root=ROOT, require_all=False):
    slots = json.loads((root / "assets/prints/manifest.json").read_text(encoding="utf-8"))
    missing = []
    for slot in slots:
        name = slot["file"]
        if Path(name).name != name or not name.endswith(".png"):
            raise ValueError("Nome de captura inválido")
        source = root / "assets/prints" / name
        pattern = re.compile(r"(<!-- print:" + re.escape(name) + r":start -->)(.*?)(<!-- print:" + re.escape(name) + r":end -->)", re.S)
        found = pattern.search(content)
        if not found:
            raise ValueError("Slot ausente: " + name)
        if not source.exists():
            missing.append(name)
            if 'class="product-print"' in found.group(2):
                raise ValueError("Captura anteriormente integrada foi removida: " + name)
            continue
        data = source.read_bytes()
        if len(data) < 24 or data[:8] != b"\x89PNG\r\n\x1a\n" or data[12:16] != b"IHDR":
            raise ValueError("PNG inválido: " + name)
        width, height = struct.unpack(">II", data[16:24])
        if width < 100 or height < 100:
            raise ValueError("Captura pequena demais: " + name)
        title = html.escape(slot["title"], quote=True)
        body = f'<figure class="device {slot["device"]}" data-print="{name}"><div class="device-bar" aria-hidden="true"><i></i><i></i><i></i><span>Tilevu · {title}</span></div><a href="assets/prints/{name}" aria-label="Ampliar captura: {title}"><img class="product-print" src="assets/prints/{name}" alt="Captura real do Tilevu: {title}" width="{width}" height="{height}" loading="lazy" decoding="async"></a><figcaption>{title}</figcaption></figure>'
        content = pattern.sub(lambda m: m.group(1) + body + m.group(3), content)
    if missing and require_all:
        raise ValueError("Capturas reais pendentes: " + ", ".join(missing))
    return content, missing

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--require-all", action="store_true")
    args = parser.parse_args()
    page = ROOT / "index.html"
    try:
        result, missing = render(page.read_text(encoding="utf-8"), require_all=args.require_all)
    except ValueError as error:
        parser.exit(1, str(error) + "\n")
    page.write_text(result, encoding="utf-8")
    print(f"Capturas pendentes: {len(missing)}")
    for name in missing:
        print(name)

if __name__ == "__main__":
    main()
