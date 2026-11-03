import pygame

from config import LARGURA, ALTURA, BLOCOS, DURACAO_TRANSICAO


class Transicao:
    def __init__(self):
        self.estado = None   # None, "saindo" (pixelando) ou "entrando" (despixelando)
        self.timer = 0.0
        self.sala_destino = None
        self.lado_entrada = None

    @property
    def ativa(self):
        return self.estado is not None

    def iniciar(self, sala_destino, lado_entrada):
        self.estado = "saindo"
        self.timer = 0.0
        self.sala_destino = sala_destino
        self.lado_entrada = lado_entrada

    def atualizar(self, dt):
        """Devolve "trocar" no pico do efeito (hora de trocar de sala) e "fim" ao terminar."""
        if not self.ativa:
            return None
        self.timer += dt
        if self.timer < DURACAO_TRANSICAO:
            return None
        self.timer = 0.0
        if self.estado == "saindo":
            self.estado = "entrando"
            return "trocar"
        self.estado = None
        return "fim"

    def desenhar(self, origem, destino):
        """Copia 'origem' em 'destino', pixelando conforme o progresso."""
        if not self.ativa:
            destino.blit(origem, (0, 0))
            return
        progresso = min(self.timer / DURACAO_TRANSICAO, 0.999)
        etapa = int(progresso * len(BLOCOS))
        if self.estado == "entrando":
            etapa = len(BLOCOS) - 1 - etapa
        bloco = BLOCOS[etapa]
        if bloco == 1:
            destino.blit(origem, (0, 0))
            return
        pequena = pygame.transform.smoothscale(
            origem, (max(1, LARGURA // bloco), max(1, ALTURA // bloco))
        )
        destino.blit(pygame.transform.scale(pequena, (LARGURA, ALTURA)), (0, 0))
