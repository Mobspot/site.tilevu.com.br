# Tilevu — site estático

O Tesseract é o mantenedor. Governança: SPEC-0030 e ADR-0014 no plano de controle Tesseract.
Somente o site estático `site.tilevu.com.br`; a aplicação `tilevu.com.br` fica fora.
Trabalhar em `landing`. Não mesclar em `main` sem revisão do CEO e autorização de produção aplicável: main publica no GitHub Pages.
Não inventar preço, clientes, depoimentos, métricas, integrações ou telas do produto.
Não gravar segredos. Testar com `python -m unittest discover -s tests -v`.
Auditoria completa usa o motor central do Tesseract e `.tesseract/quality.json`.
Antes de publicar: completar prints reais, reconciliar fatos do produto, autorização, baseline, smoke e rollback.
