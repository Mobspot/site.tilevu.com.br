# Tilevu — landing estática

Site independente `https://site.tilevu.com.br/`; login em `https://tilevu.com.br`.
Rodada mobile: branch `mobile`, baseline `acd2ab1`, por pedido autorizado
`2026-11-15_1855_ceo_landing-tilevu-mobile.md`. O CEO informou que a versão anterior
foi aprovada/publicada. Esta rodada é candidata e não autoriza merge/deploy.

## Prévia e testes

```sh
python -m http.server 8766 --bind 127.0.0.1
python scripts/optimize_prints.py
python scripts/prepare_prints.py --require-all
python -m unittest discover -s tests -v
```

Pillow é necessário somente para gerar os WebP. A página é HTML/CSS, com motion
progressivo opcional. Sem framework, rastreador ou CDN. CI também valida `mobile`.
A raiz é publicada pelo GitHub Pages somente após aprovação/merge em `main`.

## Capturas e responsividade

21 capturas novas, declaradas em `assets/prints/manifest.json`, com dados fictícios
conferidos pelo CEO. Pares 12–15 mostram o mesmo momento em computador e celular.
O contrato aceita `companion`, identificadores de posição e prioridade do herói;
o renderizador é idempotente. Os originais antigos e novos são preservados.

Herói e cards PDV/estoque usam pares reais. A galeria reúne PDV, Meu dia, ranking
e estoque. Fiscal/multi-loja conservam os textos; seus desktops sem par foram
retirados da apresentação para não inventar uma versão mobile correspondente.
Até 640 px os pares mostram só o celular. Uma fonte SVG mínima evita carregar o
desktop oculto. Nenhuma tela de produto foi gerada ou recortada para simular mobile.

`Na palma da mão` vem imediatamente após o herói: faixas de pedido (20–24) e
relatório (25–28), com etapas numeradas, região focável e scroll-snap nativo.
`Relatórios no bolso` reúne 16–19 e 14. A loja usa as fotos de 20–22.
FAQ/JSON-LD incluem celular, llms tem os novos fragmentos e sitemap tem lastmod.

WebP 720/1170 para celulares e 720/1440 para desktop, qualidade 90; alt, dimensões
e srcset/sizes. Herói eager/prioritário; demais prints lazy. As telas não são
cortadas pela altura fixa legada. Os 21 PNGs somam 4.917.344 bytes; os WebP maiores,
2.139.168 bytes (-56,5%). PNGs são acessados somente por clique.

O conjunto preservado (originais antigos/novos e variantes) ocupa cerca de 15,3 MB.
O orçamento de armazenamento passa de 8 para 16 MB por esse acréscimo explícito;
limites individuais e transferência inicial de 3 MB permanecem. Isso não é medida
de transferência em navegador. Auditar cópia sem `.git`/`__pycache__`.

## Evidência e gates

14 testes do site aprovados, inclusive referências, pares, prioridade, FAQ e
idempotência. Revisão das capturas originais em prancha feita. Chrome falhou ao
obter porta de depuração; tentativa com perfil próprio falhou com acesso negado
no crashpad; navegador conectado encerrou o kernel. Não há aprovação visual em
1440/1024/768/390, teclado, contraste computado, reduced-motion ou Lighthouse.
Evidência detalhada: SPEC-0030/mobile-evidence.md no Tesseract.

Revisão CEO, navegador/Lighthouse, reconciliação das alegações fiscal/estoque/XML,
autorização aplicável, smoke e rollback são gates de produção. Rollback desta
rodada: baseline `acd2ab1`, sem force push. A redação comercial anterior é mantida;
o Tesseract não certifica funcionamento do produto. GA4, Search Console,
conversões e relatório semanal continuam pendentes.

Fotos ilustrativas e montagem do Geladão fornecidas pelo CEO; aviso no rodapé.
Fontes DM Sans/DM Mono locais sob OFL. Marca preservada e OG 1200×630 mantido.
