# Capturas reais — rodada mobile

Fonte: 21 PNGs entregues pelo CEO, dados fictícios conferidos na origem.
12–15: pares desktop/celular; 16–19: relatórios; 20–24: pedido na loja;
25–28: consulta do relatório. Originais anteriores preservados, sem uso na página.

`manifest.json` define as posições ativas. `file`, `title`, `device` descrevem a
captura; `companion` liga a versão celular ao desktop; `id` permite reutilização
em posições diferentes; `eager` é reservado ao herói. Os marcadores `print:` no
HTML delimitam trechos regeneráveis. Não editar o HTML gerado dentro deles.

Rode `python scripts/optimize_prints.py` e depois
`python scripts/prepare_prints.py --require-all` a partir da raiz do site.
O primeiro deduplica capturas e deriva WebP; o segundo valida PNGs, gera os pares
CSS, alt, srcset e dimensões, e bloqueia fontes removidas ou inválidas.
