# Tilevu — landing estática

Candidato de `https://site.tilevu.com.br/`. Login continua em `https://tilevu.com.br`.

## Prévia e testes

```sh
python -m http.server 8765 --bind 127.0.0.1
python -m unittest discover -s tests -v
python scripts/optimize_prints.py
python scripts/prepare_prints.py
```

A raiz é publicada pelo GitHub Pages após aprovação e merge em `main`. A branch `landing` não publica. Sem build, framework, rastreador ou dependência de CDN.

## Prints reais

Ver `assets/prints/README.md`. Onze capturas reais do Laboratório foram recebidas no checkout e integradas. A captura 02 mostra pagamento, não fechamento de turno; a 10 mostra PDV móvel, não IA. Antes do release, `python scripts/prepare_prints.py --require-all` precisa passar, seguido dos testes e da revisão visual.

## Imagens e marca

Fotos ilustrativas geradas por IA e montagem do Geladão fornecidas pelo CEO em 15/11/2026. Caso autorizado por Sidney. Aviso discreto no rodapé e alt descritivo, conforme revisão 1. Símbolo e favicon fornecidos pelo Tilevu. Fontes DM Sans/DM Mono locais sob OFL (licenças em assets/fonts). Composição social própria em `assets/og-image.png` (1200×630), sem selo, renderizada por `python scripts/render_social.py` (Pillow e PyMuPDF). `scripts/og-card.html` conserva a composição alternativa para captura no navegador.

## Gates de produção

Revisão CEO, validação visual responsiva, Lighthouse, reconciliação das alegações de fiscal/estoque/XML com o dono do produto e autorização explícita. Baseline: `4ce06f4`. O candidato segue a redação comercial solicitada, sem certificar homologação fiscal nem disponibilidade funcional. Sem preços, métricas ou depoimentos inventados.
GA4, Search Console, conversões e relatório semanal pendentes no inventário Tesseract. Smoke e rollback são gates do release, não desta prévia.

## Validação desta sessão

Revisão 1: 14 testes locais e auditoria estática central aprovados. Doze capturas distintas, incluindo o extra do catálogo, zero pendentes. Chrome/Puppeteer não iniciou (EPERM/acesso negado em crashpad); navegador conectado também falhou na inicialização do sandbox. Portanto 1440/1024/768/390 px, teclado, reduced-motion no navegador e Lighthouse continuam sem aprovação nesta sessão. Não liberar produção até executar esses gates.

Herói usa `picture` para trocar o PDV desktop pelo móvel até 640 px, sem baixar os dois por CSS. Cards PDV/fiscal/multi-loja e galeria de seis telas ficam abertos. Revendedor desabilitado no cabeçalho acima de 640 px e no rodapé. Fiscal preservado por decisão explícita do CEO de 15/11 às 17:46, em nome do Sidney; não constitui validação funcional.

WebP com qualidade 90 e larguras 720/1440 (1170 no celular, sem ampliar original): 951.002 bytes para o conjunto maior versus 3.330.287 bytes dos PNGs utilizados, redução de 71,4%. Os PNGs continuam disponíveis somente por clique. Orçamento total de armazenamento passou de 6 para 8 MB para acomodar originais e derivados; limite de transferência inicial permanece 3 MB e requer Lighthouse. Auditar uma cópia da branch sem `.git`/`__pycache__`, como o artefato entregue ao Pages, nunca somar o banco de objetos Git ao peso público.
