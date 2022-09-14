import pygame as pg
import sys

# Inicializa o PyGame
pg.init()

# Função para carregar as imagens do jogo
def carregar_imagem(caminho):
    return pg.image.load(caminho).convert_alpha()

# Configurações do jogo
LARGURA = 430
ALTURA = 800
FPS = 30
VELOCIDADE = 10
GRAVIDADE = 1

# Configurações de tela
tela_jogo = pg.display.set_mode((LARGURA,ALTURA))
pg.display.set_caption('Flappy Bird')

# Relógio
relogio = pg.time.Clock()

# Imagens
bg = pg.image.load('src/bg.png')
BACKGROUND = pg.transform.scale(bg, (LARGURA,ALTURA))
img_asa_baixo = carregar_imagem('src/yellowbird-downflap.png')
img_asa_meio = carregar_imagem('src/yellowbird-midflap.png')
img_asa_cima = carregar_imagem('src/yellowbird-upflap.png')

class Passaro(pg.sprite.Sprite):
    def __init__(self):
        pg.sprite.Sprite.__init__(self)

        self.contador = 0
        self.imagens = [img_asa_baixo,img_asa_meio,img_asa_cima]
        self.image = self.imagens[self.contador]
        self.rect = self.image.get_rect()
        self.rect[0] = LARGURA / 2
        self.rect[1] = ALTURA / 2
        self.speed = VELOCIDADE

    def update(self):
        if (self.contador == len(self.imagens)-1):
            self.contador = 0
        else:
            self.contador += 1
        self.image = self.imagens[self.contador]

        self.speed += GRAVIDADE

        self.rect[1] += self.speed
    
    def voe(self):
        self.speed = -VELOCIDADE
        print(self.speed)

sprites_passaro = pg.sprite.Group()
passaro = Passaro()
sprites_passaro.add(passaro)

while True:
    for evento in pg.event.get():
        if (evento.type == pg.QUIT):
            pg.quit()
            sys.exit()
        if evento.type == pg.KEYDOWN:
            if evento.key == pg.K_SPACE:
                passaro.voe()

    tela_jogo.blit(BACKGROUND, (0,0))

    sprites_passaro.update()
    sprites_passaro.draw(tela_jogo)

    relogio.tick(FPS)
    pg.display.update()
