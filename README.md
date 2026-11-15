# Tilevu — landing estática

Candidato de `https://site.tilevu.com.br/`. Login continua em `https://tilevu.com.br`.

## Prévia e testes

```sh
python -m http.server 8765 --bind 127.0.0.1
python -m unittest discover -s tests -v
python scripts/prepare_prints.py
```

A raiz é publicada pelo GitHub Pages após aprovação e merge em `main`. A branch `landing` não publica. Sem build, framework, rastreador ou dependência de CDN.

## Prints reais

Ver `assets/prints/README.md`. Onze capturas reais do Laboratório foram recebidas no checkout e integradas. A captura 02 mostra pagamento, não fechamento de turno; a 10 mostra PDV móvel, não IA. Antes do release, `python scripts/prepare_prints.py --require-all` precisa passar, seguido dos testes e da revisão visual.

## Imagens e marca

Fotos ilustrativas geradas por IA e montagem do Geladão fornecidas pelo CEO em 15/11/2026. Caso autorizado por Sidney. Legendas distinguem ilustração de captura real. Símbolo e favicon fornecidos pelo Tilevu. Fontes DM Sans/DM Mono locais sob OFL (licenças em assets/fonts). Composição social própria em `assets/og-image.png` (1200×630), derivada do herói. `scripts/og-card.html` conserva a composição alternativa para captura no navegador.

## Gates de produção

Revisão CEO, validação visual responsiva, Lighthouse, reconciliação das alegações de fiscal/estoque/XML com o dono do produto e autorização explícita. Baseline: `4ce06f4`. O candidato segue a redação comercial solicitada, sem certificar homologação fiscal nem disponibilidade funcional. Sem preços, métricas ou depoimentos inventados.
GA4, Search Console, conversões e relatório semanal pendentes no inventário Tesseract. Smoke e rollback são gates do release, não desta prévia.

## Validação desta sessão

13 testes locais e auditoria estática central aprovados. Encaixe estrito: zero capturas pendentes. Chrome não iniciou no ambiente (EPERM/acesso negado em crashpad); Computer Use também falhou na inicialização do sandbox. Portanto 1440/1024/768/390 px, teclado, reduced-motion no navegador e Lighthouse não foram aprovados. Não liberar produção até executar esses gates.
