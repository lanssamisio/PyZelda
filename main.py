import pygame

from config import LARGURA, ALTURA, FPS, TILE, OPOSTO
from jogador import Jogador
from salas import criar_salas, verificar_saida
from transicao import Transicao


def desenhar_texto(superficie, fonte, texto, centro_x, y, cor=(255, 255, 255)):
    """Texto centralizado com sombra, para ler bem em qualquer fundo."""
    sombra = fonte.render(texto, True, (0, 0, 0))
    imagem = fonte.render(texto, True, cor)
    x = centro_x - imagem.get_width() // 2
    superficie.blit(sombra, (x + 2, y + 2))
    superficie.blit(imagem, (x, y))


def main():
    pygame.init()
    tela = pygame.display.set_mode((LARGURA, ALTURA))
    pygame.display.set_caption("Meu Zelda")
    relogio = pygame.time.Clock()
    fonte = pygame.font.Font(None, 28)
    fonte_grande = pygame.font.Font(None, 36)
    canvas = pygame.Surface((LARGURA, ALTURA))  # o jogo é desenhado aqui, depois vai para a tela

    salas = criar_salas()
    sala = salas[1]
    jogador = Jogador(12 * TILE, 15 * TILE)
    transicao = Transicao()

    mensagem = ""
    timer_mensagem = 0.0

    rodando = True
    while rodando:
        dt = relogio.tick(FPS) / 1000

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                rodando = False
            else:
                jogador.tratar_evento(evento)

        jogador.atualizar_teclas(pygame.key.get_pressed())

        if not transicao.ativa:
            jogador.atualizar(dt, sala)

            # Pegar itens
            for item in sala.itens:
                if not item.coletado and jogador.rect.colliderect(item.rect):
                    item.coletado = True
                    if item.tipo == "espada":
                        jogador.tem_espada = True
                        sala.desbloquear("leste")  # a porta da sala 1 abre
                        mensagem = "Voce pegou a espada! Aperte ESPACO para atacar."
                        timer_mensagem = 4.0

            # Saiu pela abertura? Começa a transição
            lado = verificar_saida(jogador.rect)
            if lado and lado in sala.saidas_abertas():
                transicao.iniciar(sala.saidas_abertas()[lado], OPOSTO[lado])
        else:
            resultado = transicao.atualizar(dt)
            if resultado == "trocar":
                # Tela toda pixelada: trocamos de sala sem o jogador ver
                sala = salas[transicao.sala_destino]
                jogador.posicionar_na_entrada(transicao.lado_entrada)

        if timer_mensagem > 0:
            timer_mensagem -= dt

        # --- Desenho ---
        sala.desenhar(canvas)
        jogador.desenhar(canvas)
        canvas.blit(fonte.render(sala.nome, True, (255, 255, 255)), (10, 8))

        if sala.id == 1 and not jogador.tem_espada:
            desenhar_texto(canvas, fonte_grande, "Pegue a espada no pedestal", LARGURA // 2, ALTURA - 90)
        if timer_mensagem > 0:
            desenhar_texto(canvas, fonte_grande, mensagem, LARGURA // 2, ALTURA - 90, (255, 235, 120))

        transicao.desenhar(canvas, tela)
        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()
