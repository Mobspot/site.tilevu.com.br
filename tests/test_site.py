import importlib.util
import json
import re
import struct
from unittest.mock import patch
import unittest
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlsplit
from xml.etree import ElementTree

ROOT = Path(__file__).resolve().parents[1]
CANONICAL = "https://site.tilevu.com.br/"

class Parser(HTMLParser):
    def __init__(self):
        super().__init__(); self.tags=[]; self.ids=[]; self.json_ld=[]; self.buffer=None
    def handle_starttag(self, tag, attrs):
        attrs=dict(attrs); self.tags.append((tag,attrs))
        if attrs.get('id'): self.ids.append(attrs['id'])
        if tag=='script' and attrs.get('type')=='application/ld+json': self.buffer=[]
    def handle_data(self,data):
        if self.buffer is not None: self.buffer.append(data)
    def handle_endtag(self,tag):
        if tag=='script' and self.buffer is not None:
            self.json_ld.append(json.loads(''.join(self.buffer)));self.buffer=None

class SiteTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.html=(ROOT/'index.html').read_text(encoding='utf-8'); cls.parser=Parser();cls.parser.feed(cls.html)
        cls.css=(ROOT/'assets/style.css').read_text(encoding='utf-8')
        cls.slots=json.loads((ROOT/'assets/prints/manifest.json').read_text(encoding='utf-8'))
    def test_required_files(self):
        for name in ['index.html','404.html','robots.txt','sitemap.xml','llms.txt','site.webmanifest','CNAME','.nojekyll','assets/og-image.png','.tesseract/quality.json','.github/workflows/validate.yml']:
            self.assertTrue((ROOT/name).is_file(),name)
    def test_semantics_and_encoding(self):
        self.assertIn('<html lang="pt-BR">',self.html)
        self.assertEqual(1,sum(t=='h1' for t,a in self.parser.tags))
        self.assertEqual(len(self.parser.ids),len(set(self.parser.ids)))
        self.assertIn('href="#conteudo"',self.html)
        self.assertNotIn('noindex',self.html)
        self.assertIn('Seu comércio.',self.html)
        self.assertIn('Pagamento da venda',self.html)
        self.assertNotRegex(self.html,r'[A-Za-z]\?[A-Za-z]')
        self.assertNotIn('�',self.html)
        self.assertIn(':focus-visible',self.css)
    def test_local_references_including_srcset(self):
        for file in ['index.html','404.html']:
            parser=Parser();parser.feed((ROOT/file).read_text(encoding='utf-8'))
            for tag,a in parser.tags:
                refs=[a[k] for k in ['src','href'] if a.get(k)]
                refs += [part.strip().split()[0] for part in a.get('srcset','').split(',') if part.strip()]
                for ref in refs:
                    parts=urlsplit(ref)
                    if parts.scheme: continue
                    if parts.path:
                        self.assertTrue((ROOT/parts.path.lstrip('/')).is_file(),ref)
                    elif parts.fragment:
                        self.assertIn(parts.fragment,parser.ids)
    def test_images_accessible_and_responsive(self):
        for tag,a in self.parser.tags:
            if tag!='img':continue
            self.assertTrue(a.get('alt'));self.assertTrue(a.get('width'));self.assertTrue(a.get('height'))
            if '/images/' in a.get('src',''):
                self.assertIn('srcset',a)
                self.assertTrue(a.get('loading')=='lazy' or a.get('fetchpriority')=='high')
    def test_metadata_and_social_dimensions(self):
        tags={a.get('property',a.get('name')):a.get('content') for t,a in self.parser.tags if t=='meta'}
        self.assertIn(f'<link rel="canonical" href="{CANONICAL}">',self.html)
        self.assertEqual(CANONICAL,tags['og:url'])
        self.assertEqual('summary_large_image',tags['twitter:card'])
        data=(ROOT/'assets/og-image.png').read_bytes()
        self.assertEqual((1200,630),struct.unpack('>II',data[16:24]))
    def test_faq_matches_structured_data(self):
        graph=self.parser.json_ld[0]['@graph']
        self.assertEqual({'Organization','SoftwareApplication','FAQPage'},{g['@type'] for g in graph})
        faq=next(g for g in graph if g['@type']=='FAQPage')['mainEntity']
        visible=self.html.split('</script>',1)[1]
        self.assertEqual(6,len(faq))
        for question in faq:
            self.assertIn(question['name'],visible)
            self.assertIn(question['acceptedAnswer']['text'],visible)
    def test_contact_login_and_disabled_reseller(self):
        links=[a['href'] for t,a in self.parser.tags if t=='a']
        self.assertIn('https://tilevu.com.br',links)
        self.assertGreater(links.count('mailto:contato@mobspot.com.br'),3)
        button=next(a for t,a in self.parser.tags if t=='button')
        self.assertIn('disabled',button);self.assertEqual('true',button['aria-disabled']);self.assertNotIn('href',button)
        self.assertNotIn('wa.me/',self.html)
    def test_discovery_and_404(self):
        robots=(ROOT/'robots.txt').read_text(encoding='utf-8')
        self.assertIn('Allow: /',robots);self.assertIn(CANONICAL+'sitemap.xml',robots)
        tree=ElementTree.parse(ROOT/'sitemap.xml');self.assertEqual([CANONICAL],[x.text for x in tree.findall('{*}url/{*}loc')])
        self.assertEqual('site.tilevu.com.br',(ROOT/'CNAME').read_text().strip())
        self.assertIn('noindex, nofollow',(ROOT/'404.html').read_text(encoding='utf-8'))
        self.assertIn(CANONICAL,(ROOT/'llms.txt').read_text(encoding='utf-8'))
    def test_fonts_motion_and_no_cdn(self):
        fonts=(ROOT/'assets/fonts/fonts.css').read_text(encoding='utf-8')
        for ref in re.findall(r'url\(([^)]+)\)',fonts): self.assertTrue((ROOT/'assets/fonts'/ref).is_file())
        self.assertIn('font-display: swap',fonts)
        for file in ['dmsans-OFL.txt','dmmono-OFL.txt']:self.assertTrue((ROOT/'assets/fonts'/file).is_file())
        self.assertIn('prefers-reduced-motion',self.css)
        self.assertNotIn('fonts.googleapis.com',self.html)
        self.assertNotIn('fonts.gstatic.com',fonts)
    def test_print_contract_and_review_gate(self):
        self.assertEqual(11,len(self.slots))
        for slot in self.slots:
            self.assertIn(f'data-print="{slot["file"]}"',self.html)
        manifest=json.loads((ROOT/'.tesseract/quality.json').read_text(encoding='utf-8'))
        self.assertEqual({390,768,1024,1440},{v['width'] for v in manifest['browser']['viewports']})
        self.assertIn('main, landing',(ROOT/'.github/workflows/validate.yml').read_text())
        self.assertIn('reconciliação',(ROOT/'README.md').read_text(encoding='utf-8'))
    def test_no_obvious_secrets(self):
        for p in ROOT.rglob('*'):
            if not p.is_file() or '.git' in p.parts or p.suffix not in ['.html','.md','.json','.js','.css','.yml','.txt']:continue
            text=p.read_text(encoding='utf-8')
            for pattern in [r'-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----',r'gh[pousr]_[A-Za-z0-9_]{20,}',r'AIza[0-9A-Za-z_-]{20,}']:
                self.assertIsNone(re.search(pattern,text),str(p))

class PrintIngestionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        spec=importlib.util.spec_from_file_location('prints',ROOT/'scripts/prepare_prints.py')
        cls.module=importlib.util.module_from_spec(spec);spec.loader.exec_module(cls.module)
    def test_missing_captures_keep_placeholder_and_strict_mode_blocks(self):
        content=(ROOT/'index.html').read_text(encoding='utf-8')
        # Simulate a fresh slot and missing image independently of delivered captures.
        slot=self.module.json.loads((ROOT/'assets/prints/manifest.json').read_text(encoding='utf-8'))[0]
        content=f'<!-- print:{slot["file"]}:start --><div>placeholder</div><!-- print:{slot["file"]}:end -->'
        with patch.object(self.module.json,'loads',return_value=[slot]), patch.object(Path,'exists',return_value=False):
            result,missing=self.module.render(content)
            self.assertEqual(content,result);self.assertEqual([slot['file']],missing)
            with self.assertRaises(ValueError):self.module.render(content,require_all=True)
    def test_ingestion_dimensions_idempotency_and_invalid_input(self):
        slot={'file':'01-pdv-venda.png','title':'Caixa','device':'tablet'}
        data=b'\x89PNG\r\n\x1a\n'+b'\x00\x00\x00\x0dIHDR'+struct.pack('>II',1200,800)
        content='<!-- print:01-pdv-venda.png:start --><div>placeholder</div><!-- print:01-pdv-venda.png:end -->'
        with patch.object(self.module.json,'loads',return_value=[slot]), patch.object(Path,'exists',return_value=True), patch.object(Path,'read_bytes',return_value=data):
            result,missing=self.module.render(content,require_all=True)
            self.assertEqual([],missing);self.assertIn('width="1200" height="800"',result)
            self.assertEqual(result,self.module.render(result,require_all=True)[0])
        with patch.object(self.module.json,'loads',return_value=[slot]), patch.object(Path,'exists',return_value=True), patch.object(Path,'read_bytes',return_value=b'not a png'):
            with self.assertRaises(ValueError):self.module.render(content)

if __name__=='__main__':unittest.main()
