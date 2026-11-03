TILE = 32
COLUNAS, LINHAS = 25, 20
LARGURA, ALTURA = COLUNAS * TILE, LINHAS * TILE
FPS = 60

# Posição das aberturas nas paredes (em tiles)
ABERTURA_H = range(11, 14)  # colunas das portas norte/sul
ABERTURA_V = range(8, 12)   # linhas das portas oeste/leste

COR_PAREDE = (45, 45, 55)

OPOSTO = {"norte": "sul", "sul": "norte", "leste": "oeste", "oeste": "leste"}

# Efeito de pixelização: tamanho do "pixel" a cada etapa
BLOCOS = [1, 2, 4, 8, 16, 32, 64]
DURACAO_TRANSICAO = 0.45  # segundos para pixelar (e o mesmo para voltar)
