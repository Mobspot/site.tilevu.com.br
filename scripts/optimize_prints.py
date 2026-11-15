"""Deriva WebP nítido dos PNGs originais; requer Pillow somente na preparação."""
import json
from pathlib import Path
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]

def main():
    slots = json.loads((ROOT / 'assets/prints/manifest.json').read_text(encoding='utf-8'))
    original_bytes = optimized_bytes = 0
    for slot in slots:
        source = ROOT / 'assets/prints' / slot['file']
        original_bytes += source.stat().st_size
        with Image.open(source) as image:
            for width in sorted({min(720, image.width), min(1440, image.width)}):
                target = source.with_name(f'{source.stem}-{width}.webp')
                resized = image.convert('RGB').resize((width, round(image.height * width / image.width)), Image.Resampling.LANCZOS)
                resized.save(target, 'WEBP', quality=90, method=6)
                if width == min(1440, image.width):
                    optimized_bytes += target.stat().st_size
    print(json.dumps({'original_bytes': original_bytes, 'large_webp_bytes': optimized_bytes, 'captures': len(slots)}))

if __name__ == '__main__':
    main()
