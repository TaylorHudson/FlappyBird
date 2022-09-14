import pygame as pg
import sys

# Inicializa o PyGame
pg.init()

# Função para carregar as imagens do jogo
def carregar_imagem(caminho):
    return pg.image.load(caminho).convert_alpha()

def colidiu_com_chao():
    retorno = pg.sprite.groupcollide(sprites_passaro,sprites_chao,False,False)
    if(retorno == {}):
        return False
    else:
        return True

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
bg = pg.image.load('src/imagens/bg.png')
BACKGROUND = pg.transform.scale(bg, (LARGURA,ALTURA))
img_asa_baixo = carregar_imagem('src/imagens/yellowbird-downflap.png')
img_asa_meio = carregar_imagem('src/imagens/yellowbird-midflap.png')
img_asa_cima = carregar_imagem('src/imagens/yellowbird-upflap.png')
img_base = carregar_imagem('src/imagens/base.png')
img_obstaculo = carregar_imagem('src/imagens/pipe-green.png')
img_game_over = carregar_imagem('src/imagens/gameover.png')

class Base(pg.sprite.Sprite):
    def __init__(self, largura, altura):
        pg.sprite.Sprite.__init__(self)

        self.image = img_base
        self.image = pg.transform.scale(self.image,(largura,altura))
        self.rect = self.image.get_rect()
        self.rect[1] = ALTURA - altura

    def update(self):
        self.rect[0] -= 10

        if self.rect[0] == -LARGURA:
            self.rect[0] = 0

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
    
    def voar(self):
        self.speed = -VELOCIDADE

class Obstaculo(pg.sprite.Sprite):
    def __init__(self):
        pg.sprite.Sprite.__init__(self)

        self.image = img_obstaculo
        self.rect = self.image.get_rect()
        self.rect[0] = 430

    def update(self):
        self.rect[0] -= VELOCIDADE 

sprites_passaro = pg.sprite.Group()
passaro = Passaro()
sprites_passaro.add(passaro)

sprites_obstaculo = pg.sprite.Group()
obstaculo = Obstaculo()
sprites_obstaculo.add(obstaculo)

sprites_chao = pg.sprite.Group()
chao = Base(LARGURA*2, 105)
sprites_chao.add(chao)

def loop_principal_jopo():
    while True:
        for evento in pg.event.get():
            if (evento.type == pg.QUIT):
                pg.quit()
                sys.exit()
            if evento.type == pg.KEYDOWN:
                if evento.key == pg.K_SPACE:
                    passaro.voar()

        relogio.tick(FPS)
        tela_jogo.blit(BACKGROUND, (0,0))

        sprites_passaro.update()
        sprites_chao.update()
        #sprites_obstaculo.update()

        sprites_passaro.draw(tela_jogo)
        sprites_chao.draw(tela_jogo)
        #sprites_obstaculo.draw(tela_jogo)

        if(colidiu_com_chao()):
            game_over()

        pg.display.update()

def game_over():
    while True:
        for evento in pg.event.get():
            if (evento.type == pg.QUIT):
                pg.quit()
                sys.exit()
            if evento.type == pg.KEYDOWN:
                if evento.key == pg.K_SPACE:
                    loop_principal_jopo()

        tela_jogo.blit(img_game_over,(LARGURA/3,ALTURA/3))
        pg.display.update()

loop_principal_jopo()