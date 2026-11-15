"""Renderiza o cartão social a partir das fontes locais, sem depender do Chrome."""
from io import BytesIO
from pathlib import Path
import fitz
from PIL import Image, ImageDraw, ImageFont, ImageOps

ROOT = Path(__file__).resolve().parents[1]
card = Image.new('RGB', (1200, 630), '#1e1b4b')
photo = Image.open(ROOT / 'assets/images/ia-hero-balcao-1600.webp')
photo = ImageOps.fit(photo, (550, 630), centering=(.28, .5))
card.paste(photo, (650, 0))
logo_doc = fitz.open(ROOT / 'assets/logo-padrao.svg')
pix = logo_doc[0].get_pixmap(matrix=fitz.Matrix(.6, .6), alpha=True)
logo = Image.open(BytesIO(pix.tobytes('png'))).resize((55,55), Image.Resampling.LANCZOS)
card.paste(logo, (60,60), logo)
draw = ImageDraw.Draw(card)
def text(position, value, size, color='white', weight=4):
    draw.text(position, value, font=ImageFont.truetype(str(ROOT/f'assets/fonts/font-{weight}.ttf'),size), fill=color)
text((130,60),'Tilevu',38,weight=5)
text((237,60),'.',38,'#f59e0b',5)
text((65,210),'Seu comércio.',70)
text((65,292),'Em outro nível.',70)
text((65,435),'PDV, estoque, fiscal e loja online.',25,'#cdd7ff',2)
text((65,475),'Tudo conectado. Tudo Tilevu.',25,'#cdd7ff',2)
card.save(ROOT/'assets/og-image.png', optimize=True)
print('OG renderizado: 1200x630, sem selo sobre a foto.')
