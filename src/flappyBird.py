from random import randint
import pygame as pg
import sys

# Inicializa o PyGame
pg.init()
pg.mixer.init()


def tamanho_aleatorio():
    altura_aleatoria = randint(300, 600)
    return altura_aleatoria

# Função para carregar as imagens do jogo
def carregar_imagem(caminho):
    return pg.image.load(caminho).convert_alpha()

# Funções que verificam colisões
def colidiu_com_chao():
    retorno = pg.sprite.groupcollide(sprites_passaro,sprites_chao,False,False)
    if(retorno == {}):
        return False
    else:
        return True

def colidiu_com_obstaculo():
    retorno = pg.sprite.groupcollide(sprites_passaro,sprites_obstaculo,False,False)
    if(retorno == {}):
        return False
    else:
        return True

# Função que verifica se pontuou
def pontuou():
    return obstaculo_invertido.rect[0] == 110

# Configurações do jogo
LARGURA = 430
ALTURA = 800
FPS = 30
VELOCIDADE = 10
GRAVIDADE = 1
LARGURA_OBSTACULO = 120
ALTURA_OBSTACULO = 300 
FONTE = pg.font.SysFont('Pixellari', 45)

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
img_inicial = carregar_imagem('src/imagens/pressioneespaco.png')
img_inicial = pg.transform.scale(img_inicial,(450,400))
img_nome_jogo = carregar_imagem('src/imagens/nome_jogo.png')
creditos = carregar_imagem('src/imagens/nomedogrupo.png')
creditos = pg.transform.scale(creditos, (180,150))

# Áudios
som_pontuacao = pg.mixer.Sound('src/audios/point.wav')
som_hit = pg.mixer.Sound('src/audios/hit.wav')
som_voo = pg.mixer.Sound('src/audios/som_voo.wav')
som_vento = pg.mixer.music.load('src/audios/som_vento.wav')
som_die = pg.mixer.Sound('src/audios/audio_die.wav')

# Classes dos objetos que interagem no jogo
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
    def __init__(self,invertido):
        pg.sprite.Sprite.__init__(self)

        self.altura_obstaculo = ALTURA_OBSTACULO
        self.largura_obstaculo = LARGURA_OBSTACULO

        self.image = img_obstaculo
        self.image = pg.transform.scale(self.image,(self.largura_obstaculo,500)) #self.altura_obstaculo
        self.rect = self.image.get_rect() 

        if (invertido):
            self.image = pg.transform.flip(self.image,False,True)
            self.rect[0] = LARGURA + self.largura_obstaculo
        else:
            self.rect[0] = LARGURA + self.largura_obstaculo
            self.rect[1] = 395

    def update(self):
        def tamanho_aleatorio():
            altura_aleatoria = randint(300, 400)
            return altura_aleatoria

        self.rect[0] -= VELOCIDADE
        if(self.rect[0] == -LARGURA):
            self.altura_obstaculo = tamanho_aleatorio()
            self.rect[0] = LARGURA

# Carregando todas as srites que o jogo terá
sprites_passaro = pg.sprite.Group()
passaro = Passaro()
sprites_passaro.add(passaro)

sprites_obstaculo = pg.sprite.Group()
obstaculo = Obstaculo(False)
obstaculo_invertido = Obstaculo(True)
sprites_obstaculo.add(obstaculo_invertido)
sprites_obstaculo.add(obstaculo)

sprites_chao = pg.sprite.Group()
chao = Base(LARGURA*2, 105)
sprites_chao.add(chao)

# Main da aplicação
def loop_principal_jopo():
    pontos = 0
    obstaculo_invertido.rect[0] = LARGURA + LARGURA_OBSTACULO
    obstaculo.rect[0] = LARGURA + LARGURA_OBSTACULO

    obstaculo.rect[1] = tamanho_aleatorio()
    obstaculo_invertido.rect[1] = obstaculo.rect[1] - 600

    passaro.rect[0] = LARGURA / 2
    passaro.rect[1] = ALTURA / 2

    trigger = False
    while True:
        posicao_passaro = passaro.rect[1]
        for evento in pg.event.get():
            if (evento.type == pg.QUIT):
                pg.quit()
                sys.exit()
            if evento.type == pg.KEYDOWN:
                if evento.key == pg.K_SPACE and posicao_passaro > 15:
                    som_voo.play()
                    passaro.voar()
                    trigger = True

        pontuacao = FONTE.render(str(int(pontos)), True, (255,255,255))

        relogio.tick(FPS)
        tela_jogo.blit(BACKGROUND, (0,0))
        tela_jogo.blit(pontuacao, (25,25))

        sprites_chao.update()

        if trigger:
            sprites_passaro.update()
            sprites_obstaculo.update()

        if pontuou():
            som_pontuacao.play()
            pontos += 1
            
        sprites_passaro.draw(tela_jogo)
        sprites_chao.draw(tela_jogo)
        sprites_obstaculo.draw(tela_jogo)

        if not trigger:
            tela_jogo.blit(img_inicial, (0, 400))
            tela_jogo.blit(img_nome_jogo, (70,130))
            tela_jogo.blit(creditos, (250,680))

        if(colidiu_com_chao() or colidiu_com_obstaculo()):
            som_hit.play()
            som_die.play()
            game_over()

        pg.display.update()

# Tela de game over
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

if __name__ == '__main__':
    loop_principal_jopo()