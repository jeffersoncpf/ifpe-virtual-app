# Marca IFPE Virtual

Fontes vetoriais dos ícones, splash e logos do app, geradas por `brand.py`
(símbolo IF redesenhado em grade 3×4; verde #349A46 / #2F9E41, vermelho #CA2027).

Para regenerar os PNGs (precisa de Python 3 e Playwright):

    python3 resources/ifpe/brand.py /tmp/ifpe
    node resources/ifpe/render.js /tmp/ifpe icon.svg:resources/icon.png:1024:1024:f ...

Veja os tamanhos de cada arquivo no guia de publicação.
