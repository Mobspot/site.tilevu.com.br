# Capturas reais do Laboratório

Onze capturas fornecidas no checkout durante a sessão de 15/11/2026, às 17:06. Os nomes em `manifest.json` correspondem ao pacote recebido. O arquivo 02-pdv-fechamento.png mostra o pagamento da venda, não o fechamento de turno; a legenda foi corrigida. O arquivo 10 é PDV no celular, não IA. Não há captura específica do assistente de IA nem do fechamento às cegas.

Coloque PNGs revisados nesta pasta e rode `python scripts/prepare_prints.py --require-all`. O script lê dimensões e atualiza o HTML sem JavaScript no cliente. Clique na captura para abrir a imagem completa: nos telefones, a moldura mostra o topo da captura longa.

Dados visíveis são de demonstração/Laboratório; não inserir dados reais de cliente, credenciais, certificados ou segredos. A tela fiscal informa que a emissão é próxima etapa, portanto não prova emissão em produção. Os extras recebidos são preservados, mas não entram no roteiro principal.

Após substituir capturas, executar `python scripts/optimize_prints.py` (Pillow), seguido de `python scripts/prepare_prints.py --require-all`, testes e auditoria de peso, layout e acessibilidade. O modo estrito falha sem alterar HTML caso falte um PNG. As molduras são CSS e os conteúdos são as capturas reais fornecidas.

Revisão 1: o extra do catálogo de cervejas integra a galeria aberta, totalizando doze capturas distintas. Os PNGs originais são preservados para ampliação; a página carrega WebP responsivo 720/1440 (1170 para fontes móveis menores), qualidade 90. O herói usa picture com o PDV móvel até 640 px e prioridade alta; demais prints são lazy. A galeria exibe seis legendas de 3–5 palavras. A decisão editorial fiscal foi reafirmada pelo CEO; o print continua sem provar emissão em produção.
