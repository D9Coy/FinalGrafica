# coding: utf-8
#David Beltran Coy - Oscar Miticanoy
#Librerias
import os
import pygame
import sys
from pygame.locals import *
import time
import threading
import random
#------------------------------------------------------------------------------------------------------------------------------------------------
ANCHO = 1366
ALTO = 768
BASE_PERSONAJE = 600
VELOCIDAD = +4
nivelador=0
centSeg=0
unidSeg=0
deceSeg=0
unidMin=0
deceMin=0
#------------------------------------------------------------------------------------------------------------------------------------------------
def cargarimagen(name, colorkey=False):
    try:
        image = pygame.image.load(name)
    except pygame.error, message:
        print 'No se puede cargar la imagen: ', name
        raise SystemExit, message
    image = image.convert()
    if colorkey:
        colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey, RLEACCEL)
    return (image, image.get_rect())
#------------------------------------------------------------------------------------------------------------------------------------------------
class Explocion(pygame.sprite.Sprite):
    """Representa una explosion."""
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self._load_images()
        self.step = 0
        self.delay = 2
        (self.image, self.rect) = cargarimagen('Explocion/1.png', True)
        self.rect.center = (x, y)

    def _load_images(self):
        self.frames = []
        for n in range(1, 8):
            path = 'Explocion/%d.png'
            new_image = cargarimagen(path % n, True)[0]
            self.frames.append(new_image)

    def update(self):
        self.image = self.frames[self.step]
        if self.delay < 0:
            self.delay = 2
            self.step += 1
            if self.step > 6:
                self.kill()
        else:
            self.delay -= 1
#------------------------------------------------------------------------------------------------------------------------------------------------
class TextoTiempo:
    def __init__(self, TipoFuente = 'Halo3.ttf', Tamano = 20):
        pygame.font.init()
        self.font = pygame.font.Font(TipoFuente, Tamano)
        self.size = Tamano
 
    def render(self, surface, text, color, pos):
        text = unicode(text, "UTF-8")
        x, y = pos
        for i in text.split("\r"):
            surface.blit(self.font.render(i, 1, color), (x, y))
            y += self.size 
             
def TiempoJuego():
    global centSeg, unidSeg, deceSeg, unidMin, deceMin, nivelador, ReiniciarTiempo 
    nivelador+=1
    if nivelador == 7:
       nivelador=0
       centSeg+=1
    if centSeg==9:
       centSeg=0
       unidSeg+=1
    if unidSeg==10:
       unidSeg=0
       deceSeg+=1
    if deceSeg==6:
       deceSeg=0
       unidMin+=1
    if unidMin==10:
       unidMin=0
       deceMin+=1
    if deceMin==10:
       deceMin=0
                                     
def ConcatenacionTiempo(decMin ,uniMin ,decSeg ,uniSeg ,cenSeg):  
    timeText=''
    timeText+=str(decMin)+str(uniMin)+":"+str(decSeg)+str(uniSeg)+":"+str(cenSeg)
    return timeText
#------------------------------------------------------------------------------------------------------------------------------------------------
class Personaje(pygame.sprite.Sprite):
    cambio_x = 0
    cambio_y = 0
    nivel = None
#    nivel2 = None
    posicion = None
    def __init__( self ):
        pygame.sprite.Sprite.__init__( self )
        self.Avanzar = pygame.image.load('Personajehalo.png').convert_alpha() 
        self.Retroceder = pygame.image.load('Personajehaloreverse.png').convert_alpha() 

        self.PersonajeAvanzar = {}
        self.PersonajeAvanzar[0] = (1315, 0, 90, 120) #Agacharse
        self.PersonajeAvanzar[1] = (1225, 0, 90, 120) #Saltar
        self.PersonajeAvanzar[2] = (1110, 0, 115, 120) #Disparar
        self.PersonajeAvanzar[3] = (1015, 0, 95, 120) #Quieto
        self.PersonajeAvanzar[4] = (0, 0, 90, 120)#1
        self.PersonajeAvanzar[5] = (90, 0, 90, 120)#2
        self.PersonajeAvanzar[6] = (180, 0, 100, 120)#3
        self.PersonajeAvanzar[7] = (280, 0, 110, 120)#4 
        self.PersonajeAvanzar[8] = (390, 0, 110, 120)#5 
        self.PersonajeAvanzar[9] = (500, 0, 100, 120)#6 
        self.PersonajeAvanzar[10] = (600, 0, 100, 120)#7
        self.PersonajeAvanzar[11] = (700, 0, 100, 120)#8
        self.PersonajeAvanzar[12] = (800, 0, 100, 120)#9
        self.PersonajeAvanzar[13] = (900, 0, 115, 120)#10

        self.PersonajeRetroceder = {}
        self.PersonajeRetroceder[0] = (0, 0, 90, 120) #Agacharse
        self.PersonajeRetroceder[1] = (90, 0, 90, 120) #Saltar
        self.PersonajeRetroceder[2] = (180, 0, 120, 120) #Disparar
        self.PersonajeRetroceder[3] = (300, 0, 90, 120) #Quieto
        self.PersonajeRetroceder[4] = (1320, 0, 80, 120)#10
        self.PersonajeRetroceder[5] = (1220, 0, 100, 120)#9
        self.PersonajeRetroceder[6] = (1120, 0, 100, 120)#8
        self.PersonajeRetroceder[7] = (1010, 0, 110, 120)#7
        self.PersonajeRetroceder[8] = (900, 0, 110, 120)#6
        self.PersonajeRetroceder[9] = (800, 0, 100, 120)#5 
        self.PersonajeRetroceder[10] = (700, 0, 100, 120)#4 
        self.PersonajeRetroceder[11] = (610, 0, 90, 120)#3
        self.PersonajeRetroceder[12] = (500, 0, 110, 120)#2
        self.PersonajeRetroceder[13] = (390, 0, 110, 120)#1

        self.cual = 3
        self.cuanto = 100
        self.tiempo = 0
        self.izquierda = False
        self.ObtenerDibujoPersonaje()
        self.rect = self.image.get_rect()

    def ObtenerDibujoPersonaje(self):
        if self.izquierda == True:
              self.image=self.Retroceder.subsurface(self.PersonajeRetroceder[self.cual])
        if self.izquierda == False:
              self.image=self.Avanzar.subsurface(self.PersonajeAvanzar[self.cual])
      
    def update(self): 
        if self.cual > 13:
           self.cual = 4
        self.ObtenerDibujoPersonaje()
        self.Gravedad()

        self.rect.x += self.cambio_x
        ImpactosBloques = pygame.sprite.spritecollide(self, self.nivel.ListaPlataformas, False)
        for bloque in ImpactosBloques:
            if self.cambio_x > 0:
                self.rect.right = bloque.rect.left
            elif self.cambio_x < 0:
                self.rect.left = bloque.rect.right

        self.rect.y += self.cambio_y
        ImpactosBloques = pygame.sprite.spritecollide(self, self.nivel.ListaPlataformas, False)
        for bloque in ImpactosBloques:
            if self.cambio_y > 0:
                self.rect.bottom = bloque.rect.top + 7
            elif self.cambio_y < 0:
                self.rect.top = bloque.rect.bottom
            self.cambio_y = 0

    def Gravedad(self):
        if self.cambio_y == 0:
           self.cambio_y = 1
        else:
           self.cambio_y += .35
        if self.rect.y >= BASE_PERSONAJE - self.rect.height and self.cambio_y >= 0:
           self.cambio_y = 0
           self.rect.y = BASE_PERSONAJE - self.rect.height

    def Saltar(self):
        self.rect.y += 2
        ImpactosPlataformasY = pygame.sprite.spritecollide(self, self.nivel.ListaPlataformas, False)
        self.rect.y -= 2
        if len(ImpactosPlataformasY) > 0 or self.rect.bottom >= BASE_PERSONAJE:
            self.cambio_y = -12

    def SaltarMismoPunto(self):
        self.cambio_x = 0

    def AvanzarIzquierda(self):
        self.cambio_x = -5

    def AvanzarDerecha(self):
        self.cambio_x = +5

    def Detenerse(self):
        self.cambio_x = 0

    def Agacharse(self):
        self.cambio_x = 0
#------------------------------------------------------------------------------------------------------------------------------------------------
class Personaje2(pygame.sprite.Sprite):
    cambio_x = 0
    cambio_y = 0
    nivel2 = None
    posicion = None
    def __init__( self ):
        pygame.sprite.Sprite.__init__( self )
        self.Avanzar = pygame.image.load('Personajehalo.png').convert_alpha() 
        self.Retroceder = pygame.image.load('Personajehaloreverse.png').convert_alpha() 

        self.PersonajeAvanzar = {}
        self.PersonajeAvanzar[0] = (1315, 0, 90, 120) #Agacharse
        self.PersonajeAvanzar[1] = (1225, 0, 90, 120) #Saltar
        self.PersonajeAvanzar[2] = (1110, 0, 115, 120) #Disparar
        self.PersonajeAvanzar[3] = (1015, 0, 95, 120) #Quieto
        self.PersonajeAvanzar[4] = (0, 0, 90, 120)#1
        self.PersonajeAvanzar[5] = (90, 0, 90, 120)#2
        self.PersonajeAvanzar[6] = (180, 0, 100, 120)#3
        self.PersonajeAvanzar[7] = (280, 0, 110, 120)#4 
        self.PersonajeAvanzar[8] = (390, 0, 110, 120)#5 
        self.PersonajeAvanzar[9] = (500, 0, 100, 120)#6 
        self.PersonajeAvanzar[10] = (600, 0, 100, 120)#7
        self.PersonajeAvanzar[11] = (700, 0, 100, 120)#8
        self.PersonajeAvanzar[12] = (800, 0, 100, 120)#9
        self.PersonajeAvanzar[13] = (900, 0, 115, 120)#10

        self.PersonajeRetroceder = {}
        self.PersonajeRetroceder[0] = (0, 0, 90, 120) #Agacharse
        self.PersonajeRetroceder[1] = (90, 0, 90, 120) #Saltar
        self.PersonajeRetroceder[2] = (180, 0, 120, 120) #Disparar
        self.PersonajeRetroceder[3] = (300, 0, 90, 120) #Quieto
        self.PersonajeRetroceder[4] = (1320, 0, 80, 120)#10
        self.PersonajeRetroceder[5] = (1220, 0, 100, 120)#9
        self.PersonajeRetroceder[6] = (1120, 0, 100, 120)#8
        self.PersonajeRetroceder[7] = (1010, 0, 110, 120)#7
        self.PersonajeRetroceder[8] = (900, 0, 110, 120)#6
        self.PersonajeRetroceder[9] = (800, 0, 100, 120)#5 
        self.PersonajeRetroceder[10] = (700, 0, 100, 120)#4 
        self.PersonajeRetroceder[11] = (610, 0, 90, 120)#3
        self.PersonajeRetroceder[12] = (500, 0, 110, 120)#2
        self.PersonajeRetroceder[13] = (390, 0, 110, 120)#1

        self.cual = 3
        self.cuanto = 100
        self.tiempo = 0
        self.izquierda = False
        self.ObtenerDibujoPersonaje()
        self.rect = self.image.get_rect()

    def ObtenerDibujoPersonaje(self):
        if self.izquierda == True:
              self.image=self.Retroceder.subsurface(self.PersonajeRetroceder[self.cual])
        if self.izquierda == False:
              self.image=self.Avanzar.subsurface(self.PersonajeAvanzar[self.cual])
      
    def update(self): 
        if self.cual > 13:
           self.cual = 4
        self.ObtenerDibujoPersonaje()
        self.Gravedad()

        self.rect.x += self.cambio_x
        ImpactosBloques2 = pygame.sprite.spritecollide(self, self.nivel2.ListaPlataformas2, False)
        for bloque in ImpactosBloques2:
            if self.cambio_x > 0:
                self.rect.right = bloque.rect.left
            elif self.cambio_x < 0:
                self.rect.left = bloque.rect.right

        self.rect.y += self.cambio_y
        ImpactosBloques2 = pygame.sprite.spritecollide(self, self.nivel2.ListaPlataformas2, False)
        for bloque in ImpactosBloques2:
            if self.cambio_y > 0:
                self.rect.bottom = bloque.rect.top + 7
            elif self.cambio_y < 0:
                self.rect.top = bloque.rect.bottom
            self.cambio_y = 0

    def Gravedad(self):
        if self.cambio_y == 0:
           self.cambio_y = 1
        else:
           self.cambio_y += .35
        if self.rect.y >= BASE_PERSONAJE - self.rect.height and self.cambio_y >= 0:
           self.cambio_y = 0
           self.rect.y = BASE_PERSONAJE - self.rect.height

    def Saltar(self):
        self.rect.y += 2
        ImpactosPlataformasY2 = pygame.sprite.spritecollide(self, self.nivel2.ListaPlataformas2, False)
        self.rect.y -= 2
        if len(ImpactosPlataformasY2) > 0 or self.rect.bottom >= BASE_PERSONAJE:
            self.cambio_y = -12

    def SaltarMismoPunto(self):
        self.cambio_x = 0

    def AvanzarIzquierda(self):
        self.cambio_x = -5

    def AvanzarDerecha(self):
        self.cambio_x = +5

    def Detenerse(self):
        self.cambio_x = 0

    def Agacharse(self):
        self.cambio_x = 0
#------------------------------------------------------------------------------------------------------------------------------------------------
class DisparoDerecha( pygame.sprite.Sprite ):
    def __init__( self, posx, posy):
        pygame.sprite.Sprite.__init__( self )
        self.image = pygame.image.load('BalaDerecha.png').convert_alpha() 
        self.rect = self.image.get_rect()
        self.rect.x = posx
        self.rect.y = posy

    def update( self ):
        self.rect.move_ip((10,0))
        if self.rect.left >= ANCHO or EliminarDisparo == True:
           self.kill()

class DisparoIzquierda( pygame.sprite.Sprite ):
    def __init__( self, posx, posy):
        pygame.sprite.Sprite.__init__( self )
        self.image = pygame.image.load('BalaIzquierda.png').convert_alpha() 
        self.rect = self.image.get_rect()
        self.rect.x = posx
        self.rect.y = posy

    def update( self ):
        self.rect.move_ip((-10,0))
        if self.rect.right <= 0 or EliminarDisparo == True:
           self.kill()
#------------------------------------------------------------------------------------------------------------------------------------------------
class DisparoDerechaEnemy( pygame.sprite.Sprite ):
    def __init__( self, posx, posy):
        pygame.sprite.Sprite.__init__( self )
        self.image = pygame.image.load('BalaDerecha.png').convert_alpha() 
        self.rect = self.image.get_rect()
        self.rect.x = posx
        self.rect.y = posy

    def update( self ):
        self.rect.move_ip((10,0))
        if self.rect.left >= ANCHO or EliminarDisparo == True:
           self.kill()
#------------------------------------------------------------------------------------------------------------------------------------------------
class FondoAnimado( pygame.sprite.Sprite ):
    def __init__( self, posx, posy):
        pygame.sprite.Sprite.__init__(self)
        self.imagen_base = pygame.image.load('Fondonivel1.png').convert_alpha() 
        self.image = self.imagen_base
        self.rect = self.image.get_rect()
        self.rect.topleft = (posx,posy)

    def update( self ):
        if scroll:
           if FondoDerecha == True:
              if self.rect.right <= ANCHO:
                 self.rect.right = ANCHO
                 personaje.AvanzarDerecha()
              else:
                 self.rect.move_ip(-VELOCIDAD,0)
           if FondoDerecha == False:
              if self.rect.left >= 0:
                 self.rect.left = 0
                 personaje.AvanzarIzquierda()
              else:
                 self.rect.move_ip(VELOCIDAD,0)
#------------------------------------------------------------------------------------------------------------------------------------------------
class FondoAnimado2( pygame.sprite.Sprite ):
    def __init__( self, posx, posy):
        pygame.sprite.Sprite.__init__(self)
        self.imagen_base = pygame.image.load('Fondonivel2.png').convert_alpha() 
        self.image = self.imagen_base
        self.rect = self.image.get_rect()
        self.rect.topleft = (posx,posy)

    def update( self ):
        if movimiento2 == True:
           if FondoDerecha2 == True:
              if self.rect.right <= ANCHO:
                 self.rect.right = ANCHO
                 personaje2.AvanzarDerecha()
              else:
                 self.rect.move_ip(-VELOCIDAD,0)
           if FondoDerecha2 == False:
              if self.rect.left >= 0:
                 self.rect.left = 0
                 personaje2.AvanzarIzquierda()
              else:
                 self.rect.move_ip(VELOCIDAD,0)
#------------------------------------------------------------------------------------------------------------------------------------------------
class Plataforma(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('puente.png').convert_alpha()   
        self.rect = self.image.get_rect()

    def update(self):
        if scroll:
           if FondoDerecha == True:
              if personaje.rect.x > 680:
                 self.rect.move_ip(0,0)
              else:
                 self.rect.move_ip(-VELOCIDAD,0)
           if FondoDerecha == False:
              if personaje.rect.x < 680:
                 self.rect.move_ip(0,0)
              else:
                 self.rect.move_ip(VELOCIDAD,0)
                 
class PlataformasNivel1(pygame.sprite.Sprite):
    def __init__(self):
        self.ListaPlataformas = pygame.sprite.Group()
        nivel = [[950, 400],
                 [1018, 330],
                 [1155, 330],
                 [1245, 360],
                 [1900, 324],
                 [1900, 600],
                 [1900, 500],
                 [1900, 400],
                 [2260, 368],
                 [2458, 302],
                 [2585, 275],
                 [3195, 396],
                 [3030, 330],
                 [4675, 610],
                 [4999, 616],
                 [5296, 621],
                 [5500, 621],
                 [5780, 621],
                 [6066, 621]]

        for plataforma in nivel:
            bloque = Plataforma()
            bloque.rect.x = plataforma[0]
            bloque.rect.y = plataforma[1]
            self.ListaPlataformas.add(bloque) 

    def update(self):
        self.ListaPlataformas.update()
     
    def draw(self, pantalla):
        self.ListaPlataformas.draw(pantalla)      
#------------------------------------------------------------------------------------------------------------------------------------------------
class Plataforma2(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('Plataforma.png').convert_alpha()   
        self.rect = self.image.get_rect()

    def update(self):
        if movimiento2 == True:
           if FondoDerecha2 == True:
              if personaje2.rect.x > 680:
                 self.rect.move_ip(0,0)
              else:
                 self.rect.move_ip(-VELOCIDAD,0)
           if FondoDerecha2 == False:
              if personaje2.rect.x < 680:
                 self.rect.move_ip(0,0)
              else:
                 self.rect.move_ip(VELOCIDAD,0)

class PlataformasNivel2(pygame.sprite.Sprite):
    def __init__(self):
        self.ListaPlataformas2 = pygame.sprite.Group()
        nivel2 = [[-70, 600],
                  [980,390],
                  [2320,400],
                  [2580,200],
                  [2974,200],
                  [3324,200],
                  [4060,200],
                  [3760,340],
                  [5360,230],
                  [5780,340],
                  [6130,250],
                  [6530,250],
                  [6930,250],
                  [7310,250],
                  [70, 600],
                  [210, 600],
                  [350, 600],
                  [490, 600],
                  [640, 600],
                  [770, 600],
                  [910, 600],
                  [1050, 600],
                  [1190, 600],
                  [1330, 600],
                  [1470, 600],
                  [1610, 600],
                  [1750, 600],
                  [1890, 600],
                  [2030, 600],
                  [2170, 600],
                  [2310, 600],
                  [2450, 600],
                  [2590, 600],
                  [2730, 600],
                  [2870, 600],
                  [3010, 600],
                  [3150, 600],
                  [3290, 600],
                  [3430, 600],
                  [3570, 600],
                  [3710, 600],
                  [3850, 600],
                  [3990, 600],
                  [4130, 600],
                  [4270, 600],
                  [4410, 600],
                  [4550, 600],
                  [4690, 600],
                  [4830, 600],
                  [4970, 600],
                  [5110, 600],
                  [5250, 600],
                  [5390, 600],
                  [5530, 600],
                  [5670, 600],
                  [5810, 600],
                  [5850, 600],
                  [5990, 600],
                  [6130, 600],
                  [6270, 600],
                  [6410, 600],
                  [6550, 600],
                  [6690, 600],
                  [6830, 600],
                  [6970, 600],
                  [7110, 600],
                  [7250, 600],
                  [7390, 600],
                  [7530, 600],
                  [7570, 600]]
        for plataforma2 in nivel2:
            bloque2 = Plataforma2()
            bloque2.rect.x = plataforma2[0]
            bloque2.rect.y = plataforma2[1]
            self.ListaPlataformas2.add(bloque2) 

    def update(self):
        self.ListaPlataformas2.update()
     
    def draw(self, pantalla):
        self.ListaPlataformas2.draw(pantalla)

#------------------------------------------------------------------------------------------------------------------------------------------------
class Llamas(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('llama2.png').convert_alpha()   
        self.rect = self.image.get_rect()

    def update(self):
        if movimiento2 == True:
           if FondoDerecha2 == True:
              if personaje2.rect.x > 680:
                 self.rect.move_ip(0,0)
              else:
                 self.rect.move_ip(-VELOCIDAD,0)
           if FondoDerecha2 == False:
              if personaje2.rect.x < 680:
                 self.rect.move_ip(0,0)
              else:
                 self.rect.move_ip(VELOCIDAD,0)

class LlamasNivel2(pygame.sprite.Sprite):
    def __init__(self):
        self.ListaLlamas = pygame.sprite.Group()
        Llamas2 = [[630, 500],
                   [1180,500],
                   [2520,500],
                   [2620,500],
                   [2850,500],
                   [2900,500],
                   [3194,500],
                   [3454,500],
                   [4260,500],
                   [5600,500],
                   [6330,500],
                   [6470,500],
                   [6730,500],
                   [6870,500],
                   [7210,500],
                   [7130,500]]
        for plataforma2 in Llamas2:
            vacio2 = Llamas()
            vacio2.rect.x = plataforma2[0]
            vacio2.rect.y = plataforma2[1]
            self.ListaLlamas.add(vacio2) 

    def update(self):
        self.ListaLlamas.update()
     
    def draw(self, pantalla):
        self.ListaLlamas.draw(pantalla)

#------------------------------------------------------------------------------------------------------------------------------------------------
class YellowGrunt(pygame.sprite.Sprite):
    def __init__(self, posX, posY):
        pygame.sprite.Sprite.__init__(self)
        self.YellowGrunt1 = pygame.image.load("Gruntamarillo.png").convert_alpha()
        self.YellowGrunt2 = pygame.image.load("Gruntamarilloizq.png").convert_alpha()#pygame.transform.flip(self.YellowGrunt1, True, False)
        
        self.yellowgrunt1 = {}
        self.yellowgrunt1[0] = (0, 0, 60, 82)
        self.yellowgrunt1[1] = (60, 0, 70, 82)
        self.yellowgrunt1[2] = (130, 0, 60, 82)
        self.yellowgrunt1[3] = (190, 0, 70, 82)
        self.yellowgrunt1[4] = (260, 0, 70, 82)
        self.yellowgrunt1[5] = (330, 0, 70, 82)
        self.yellowgrunt1[6] = (400, 0, 63, 82)
        self.yellowgrunt1[7] = (463, 0, 77, 82)
        self.yellowgrunt1[8] = (540, 0, 89, 82)

        self.yellowgrunt2 = {}
        self.yellowgrunt2[0] = (566, 0, 63, 82)
        self.yellowgrunt2[1] = (500, 0, 66, 82)
        self.yellowgrunt2[2] = (440, 0, 60, 82)
        self.yellowgrunt2[3] = (370, 0, 70, 82)
        self.yellowgrunt2[4] = (300, 0, 70, 82)
        self.yellowgrunt2[5] = (230, 0, 70, 82)
        self.yellowgrunt2[6] = (166, 0, 64, 82)
        self.yellowgrunt2[7] = (80, 0, 86, 82)
        self.yellowgrunt2[8] = (0, 0, 80, 82)
        
        self.actualizacion = pygame.time.get_ticks()
        self.cual = 0     
        self.izquierda = False   
        self.obtenerDibujo()
        self.rect = self.image.get_rect()
        self.rect.topleft = (posX, posY)
        self.dx = 1
        self.PosicionX = posX

    def obtenerDibujo(self):
        if self.izquierda:
            self.image=self.YellowGrunt2.subsurface(self.yellowgrunt2[self.cual])
        else:
            self.image=self.YellowGrunt1.subsurface(self.yellowgrunt1[self.cual])

    def update(self):
        if self.actualizacion + 100 < pygame.time.get_ticks():
           self.cual += 1
           if self.cual > 8:
              self.cual = 0
           self.obtenerDibujo()
           self.actualizacion= pygame.time.get_ticks()
        
        TiempoMovimiento =pygame.time.get_ticks()/1000         
        t = TiempoMovimiento
        if t==2 or t==6 or t==10 or t==14 or t==18 or t==22 or t==26 or t==30 or t==34 or t==38 or t==42 or t==46 or t==50 or t==54 or t==58 or t==62 or t==66 or t==70 or t==74 or t==78 or t==82 or t==86 or t==90 or t==94 or t==98 or t==102 or t==106 or t==110 or t==114 or t==118 or t==122 or t==126 or t==130 or t==134 or t==138 or t==142 or t==146 or t==150 or t==154 or t==158 or t==162  or t==166 or t==170 or t==174 or t==178 or t==182 or t==186 or t==190 or t==194 or t==198 or t==202:
           self.izquierda = True

                
        if t==4 or t==8 or t==12 or t==16 or t==20 or t==24 or t==28 or t==32 or t==36 or t==40 or t==44 or t==48 or t==52 or t==56 or t==60 or t==64 or t==68 or t==72 or t==76 or t==80 or t==84 or t==88 or t==92 or t==96 or t==100 or t==104 or t==108 or t==112 or t==116 or t==120 or t==124 or t==128 or t==132 or t==136 or t==140 or t==144 or t==148 or t==152 or t==156 or t==160 or t==164 or t==168 or t==172 or t==176 or t==180 or t==184 or t==188 or t==192 or t==196 or t==200 or t==204:
           self.izquierda = False

        if self.izquierda == True:
           self.rect.move_ip(-self.dx,0)
        else:
           self.rect.move_ip(self.dx,0)

        if scroll:
           if FondoDerecha == True:
              if personaje.rect.x > 680:
                 self.rect.move_ip(0,0)
              else:
                 self.rect.move_ip(-VELOCIDAD,0)
           if FondoDerecha == False:
              if personaje.rect.x < 680:
                 self.rect.move_ip(0,0)
              else:
                 self.rect.move_ip(VELOCIDAD,0)

class YellowGruntNivel1(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.ListaYellowGrunt = pygame.sprite.Group()

        posicionyellowgrunt = [[517, 490],
                          [1170, 490],
                          [2200, 490],
                          [2340, 278],
                          [3295, 305],
                          [1800, 490],
                          [1170, 250],
                          [1290, 270],
                          [1045, 330],
                          [5120, 510],
                          [4750, 510],
                          [5820, 510],
                          [6420, 510],
                          [6920, 510],
                          [7420, 510],
                          [3900, 490]]
        for recorrido in posicionyellowgrunt:
            yellowgrunt = YellowGrunt(recorrido[0],recorrido[1])
            self.ListaYellowGrunt.add(yellowgrunt) 

    def update(self):
        self.ListaYellowGrunt.update()
     
    def draw(self, pantalla):
        self.ListaYellowGrunt.draw(pantalla) 
#------------------------------------------------------------------------------------------------------------------------------------------------
class RedGrunt(pygame.sprite.Sprite):
    def __init__(self, posX, posY):
        pygame.sprite.Sprite.__init__(self)
        self.RedGrunt1 = pygame.image.load("Gruntrojoder.png").convert_alpha()
        self.RedGrunt2 = pygame.image.load("Gruntrojo.png").convert_alpha()
        
        self.redgrunt1 = {}
        self.redgrunt1[0] = (0, 0, 70, 82)
        self.redgrunt1[1] = (70, 0, 60, 82)
        self.redgrunt1[2] = (130, 0, 60, 82)
        self.redgrunt1[3] = (190, 0, 70, 82)
        self.redgrunt1[4] = (260, 0, 70, 82)
        self.redgrunt1[5] = (330, 0, 70, 82)
        self.redgrunt1[6] = (400, 0, 70, 82)
        self.redgrunt1[7] = (470, 0, 80, 82)
        self.redgrunt1[8] = (550, 0, 84, 82)

        self.redgrunt2 = {}
        self.redgrunt2[0] = (570, 0, 64, 82)
        self.redgrunt2[1] = (510, 0, 60, 82)
        self.redgrunt2[2] = (444, 0, 66, 82)
        self.redgrunt2[3] = (370, 0, 74, 82)
        self.redgrunt2[4] = (300, 0, 70, 82)
        self.redgrunt2[5] = (240, 0, 60, 82)
        self.redgrunt2[6] = (170, 0, 70, 82)
        self.redgrunt2[7] = (90, 0, 80, 82)
        self.redgrunt2[8] = (0, 0, 90, 82)
        
        self.actualizacion = pygame.time.get_ticks()
        self.cual = 0     
        self.izquierda = False   
        self.obtenerDibujo()
        self.rect = self.image.get_rect()
        self.rect.topleft = (posX, posY)
        self.dx = 1
        self.PosicionX = posX

    def obtenerDibujo(self):
        if self.izquierda:
           self.image=self.RedGrunt2.subsurface(self.redgrunt2[self.cual])
        else:
           self.image=self.RedGrunt1.subsurface(self.redgrunt1[self.cual])

    def update(self):
        if self.actualizacion + 100 < pygame.time.get_ticks():
           self.cual += 1
           if self.cual > 8:
              self.cual = 0
           if self.cual == 4:
              disparoenemigo = True
           self.obtenerDibujo()
           self.actualizacion= pygame.time.get_ticks()
        
        TiempoMovimiento =pygame.time.get_ticks()/1000         
        t = TiempoMovimiento
        if t==2 or t==6 or t==10 or t==14 or t==18 or t==22 or t==26 or t==30 or t==34 or t==38 or t==42 or t==46 or t==50 or t==54 or t==58 or t==62 or t==66 or t==70 or t==74 or t==78 or t==82 or t==86 or t==90 or t==94 or t==98 or t==102 or t==106 or t==110 or t==114 or t==118 or t==122 or t==126 or t==130 or t==134 or t==138 or t==142 or t==146 or t==150 or t==154 or t==158 or t==162  or t==166 or t==170 or t==174 or t==178 or t==182 or t==186 or t==190 or t==194 or t==198 or t==202:
           self.izquierda = True

                
        if t==4 or t==8 or t==12 or t==16 or t==20 or t==24 or t==28 or t==32 or t==36 or t==40 or t==44 or t==48 or t==52 or t==56 or t==60 or t==64 or t==68 or t==72 or t==76 or t==80 or t==84 or t==88 or t==92 or t==96 or t==100 or t==104 or t==108 or t==112 or t==116 or t==120 or t==124 or t==128 or t==132 or t==136 or t==140 or t==144 or t==148 or t==152 or t==156 or t==160 or t==164 or t==168 or t==172 or t==176 or t==180 or t==184 or t==188 or t==192 or t==196 or t==200 or t==204:
           self.izquierda = False

        if self.izquierda == True:
           self.rect.move_ip(-self.dx,0)
        else:
           self.rect.move_ip(self.dx,0)

        if scroll:
           if FondoDerecha == True:
              if personaje.rect.x > 680:
                 self.rect.move_ip(0,0)
              else:
                 self.rect.move_ip(-VELOCIDAD,0)
           if FondoDerecha == False:
              if personaje.rect.x < 680:
                 self.rect.move_ip(0,0)
              else:
                 self.rect.move_ip(VELOCIDAD,0)

class RedGruntNivel1(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.ListaRedGrunt = pygame.sprite.Group()

        posicionredgrunt = [[1530, 490],
                            [2000, 230],
                            [2685, 185],
                            [2845, 490],
                            [2420, 490],
                            [6700, 490],
                            [3460, 490],
                            [5920, 510],
                            [5420, 510]]
        for recorrido in posicionredgrunt:
            redgrunt = RedGrunt(recorrido[0],recorrido[1])
            self.ListaRedGrunt.add(redgrunt) 

    def update(self):
        self.ListaRedGrunt.update()
     
    def draw(self, pantalla):
        self.ListaRedGrunt.draw(pantalla) 
#------------------------------------------------------------------------------------------------------------------------------------------------
class Elite(pygame.sprite.Sprite):
    def __init__(self, posX, posY):
        pygame.sprite.Sprite.__init__(self)
        self.elite1 = pygame.image.load("Eliteder.png").convert_alpha()
        self.elite2 = pygame.image.load("Eliteizq.png").convert_alpha()
        
        self.Elite1 = {}
        self.Elite1[0] = (0, 0, 140, 127)
        self.Elite1[1] = (140, 0, 110, 127)
        self.Elite1[2] = (250, 0, 130, 127)
        self.Elite1[3] = (380, 0, 95, 127)
        self.Elite1[4] = (475, 0, 95, 127)
        self.Elite1[5] = (570, 0, 100, 127)
        self.Elite1[6] = (670, 0, 90, 127)
        self.Elite1[7] = (760, 0, 100, 127)
        self.Elite1[8] = (860, 0, 104, 127)

        self.Elite2 = {}
        self.Elite2[0] = (830, 0, 134, 127)
        self.Elite2[1] = (710, 0, 120, 127)
        self.Elite2[2] = (580, 0, 130, 127)
        self.Elite2[3] = (490, 0, 90, 127)
        self.Elite2[4] = (395, 0, 95, 127)
        self.Elite2[5] = (290, 0, 105, 127)
        self.Elite2[6] = (200, 0, 90, 127)
        self.Elite2[7] = (110, 0, 90, 127)
        self.Elite2[8] = (0, 0, 110, 127)
        
        self.actualizacion = pygame.time.get_ticks()
        self.cual = 0     
        self.izquierda = False   
        self.obtenerDibujo()
        self.rect = self.image.get_rect()
        self.rect.topleft = (posX, posY)
        self.dx = 1
        self.PosicionX = posX

    def obtenerDibujo(self):
        if self.izquierda:
            self.image=self.elite2.subsurface(self.Elite2[self.cual])
        else:
            self.image=self.elite1.subsurface(self.Elite1[self.cual])

    def update(self):
        if self.actualizacion + 100 < pygame.time.get_ticks():
           self.cual += 1
           if self.cual > 8:
              self.cual = 0
           self.obtenerDibujo()
           self.actualizacion= pygame.time.get_ticks()
        
        TiempoMovimiento =pygame.time.get_ticks()/1000         
        t = TiempoMovimiento
        if t==2 or t==6 or t==10 or t==14 or t==18 or t==22 or t==26 or t==30 or t==34 or t==38 or t==42 or t==46 or t==50 or t==54 or t==58 or t==62 or t==66 or t==70 or t==74 or t==78 or t==82 or t==86 or t==90 or t==94 or t==98 or t==102 or t==106 or t==110 or t==114 or t==118 or t==122 or t==126 or t==130 or t==134 or t==138 or t==142 or t==146 or t==150 or t==154 or t==158 or t==162  or t==166 or t==170 or t==174 or t==178 or t==182 or t==186 or t==190 or t==194 or t==198 or t==202:
           self.izquierda = True

                
        if t==4 or t==8 or t==12 or t==16 or t==20 or t==24 or t==28 or t==32 or t==36 or t==40 or t==44 or t==48 or t==52 or t==56 or t==60 or t==64 or t==68 or t==72 or t==76 or t==80 or t==84 or t==88 or t==92 or t==96 or t==100 or t==104 or t==108 or t==112 or t==116 or t==120 or t==124 or t==128 or t==132 or t==136 or t==140 or t==144 or t==148 or t==152 or t==156 or t==160 or t==164 or t==168 or t==172 or t==176 or t==180 or t==184 or t==188 or t==192 or t==196 or t==200 or t==204:
           self.izquierda = False

        if self.izquierda == True:
           self.rect.move_ip(-self.dx,0)
        else:
           self.rect.move_ip(self.dx,0)

        if scroll:
           if FondoDerecha == True:
              if personaje.rect.x > 680:
                 self.rect.move_ip(0,0)
              else:
                 self.rect.move_ip(-VELOCIDAD,0)
           if FondoDerecha == False:
              if personaje.rect.x < 680:
                 self.rect.move_ip(0,0)
              else:
                 self.rect.move_ip(VELOCIDAD,0)

class EliteNivel1(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.ListaElite = pygame.sprite.Group()

        posicionelite = [[3010, 490],
                          [3120, 210],
                          [3300, 490],
                          [5520, 490],
                          [6200, 490],
                          [6700, 490],
                          [7700, 490],
                          [8000, 490],
                          [4500, 490]]
        for recorrido in posicionelite:
            elite = Elite(recorrido[0],recorrido[1])
            self.ListaElite.add(elite) 

    def update(self):
        self.ListaElite.update()
     
    def draw(self, pantalla):
        self.ListaElite.draw(pantalla) 
#------------------------------------------------------------------------------------------------------------------------------------------------
#--------------------------------------------------------------ENEMIGOS NIVEL DOS----------------------------------------------------------------
#------------------------------------------------------------------------------------------------------------------------------------------------
class YellowGrunt2(pygame.sprite.Sprite):
    def __init__(self, posX, posY):
        pygame.sprite.Sprite.__init__(self)
        self.YellowGrunt1 = pygame.image.load("Gruntamarillo.png").convert_alpha()
        self.YellowGrunt2 = pygame.image.load("Gruntamarilloizq.png").convert_alpha()#pygame.transform.flip(self.YellowGrunt1, True, False)
        
        self.yellowgrunt1 = {}
        self.yellowgrunt1[0] = (0, 0, 60, 82)
        self.yellowgrunt1[1] = (60, 0, 70, 82)
        self.yellowgrunt1[2] = (130, 0, 60, 82)
        self.yellowgrunt1[3] = (190, 0, 70, 82)
        self.yellowgrunt1[4] = (260, 0, 70, 82)
        self.yellowgrunt1[5] = (330, 0, 70, 82)
        self.yellowgrunt1[6] = (400, 0, 63, 82)
        self.yellowgrunt1[7] = (463, 0, 77, 82)
        self.yellowgrunt1[8] = (540, 0, 89, 82)

        self.yellowgrunt2 = {}
        self.yellowgrunt2[0] = (566, 0, 63, 82)
        self.yellowgrunt2[1] = (500, 0, 66, 82)
        self.yellowgrunt2[2] = (440, 0, 60, 82)
        self.yellowgrunt2[3] = (370, 0, 70, 82)
        self.yellowgrunt2[4] = (300, 0, 70, 82)
        self.yellowgrunt2[5] = (230, 0, 70, 82)
        self.yellowgrunt2[6] = (166, 0, 64, 82)
        self.yellowgrunt2[7] = (80, 0, 86, 82)
        self.yellowgrunt2[8] = (0, 0, 80, 82)
        
        self.actualizacion = pygame.time.get_ticks()
        self.cual = 0     
        self.izquierda = False   
        self.obtenerDibujo()
        self.rect = self.image.get_rect()
        self.rect.topleft = (posX, posY)
        self.dx = 1
        self.PosicionX = posX

    def obtenerDibujo(self):
        if self.izquierda:
            self.image=self.YellowGrunt2.subsurface(self.yellowgrunt2[self.cual])
        else:
            self.image=self.YellowGrunt1.subsurface(self.yellowgrunt1[self.cual])

    def update(self):
        if self.actualizacion + 100 < pygame.time.get_ticks():
           self.cual += 1
           if self.cual > 8:
              self.cual = 0
           self.obtenerDibujo()
           self.actualizacion= pygame.time.get_ticks()
        
        TiempoMovimiento =pygame.time.get_ticks()/1000         
        t = TiempoMovimiento
        if t==2 or t==6 or t==10 or t==14 or t==18 or t==22 or t==26 or t==30 or t==34 or t==38 or t==42 or t==46 or t==50 or t==54 or t==58 or t==62 or t==66 or t==70 or t==74 or t==78 or t==82 or t==86 or t==90 or t==94 or t==98 or t==102 or t==106 or t==110 or t==114 or t==118 or t==122 or t==126 or t==130 or t==134 or t==138 or t==142 or t==146 or t==150 or t==154 or t==158 or t==162  or t==166 or t==170 or t==174 or t==178 or t==182 or t==186 or t==190 or t==194 or t==198 or t==202:
           self.izquierda = True

                
        if t==4 or t==8 or t==12 or t==16 or t==20 or t==24 or t==28 or t==32 or t==36 or t==40 or t==44 or t==48 or t==52 or t==56 or t==60 or t==64 or t==68 or t==72 or t==76 or t==80 or t==84 or t==88 or t==92 or t==96 or t==100 or t==104 or t==108 or t==112 or t==116 or t==120 or t==124 or t==128 or t==132 or t==136 or t==140 or t==144 or t==148 or t==152 or t==156 or t==160 or t==164 or t==168 or t==172 or t==176 or t==180 or t==184 or t==188 or t==192 or t==196 or t==200 or t==204:
           self.izquierda = False

        if self.izquierda == True:
           self.rect.move_ip(-self.dx,0)
        else:
           self.rect.move_ip(self.dx,0)

        if movimiento2 == True:
           if FondoDerecha2 == True:
              if personaje2.rect.x > 680:
                 self.rect.move_ip(0,0)
              else:
                 self.rect.move_ip(-VELOCIDAD,0)
           if FondoDerecha2 == False:
              if personaje2.rect.x < 680:
                 self.rect.move_ip(0,0)
              else:
                 self.rect.move_ip(VELOCIDAD,0)

class YellowGruntNivel2(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.ListaYellowGrunt2 = pygame.sprite.Group()

        posicionyellowgrunt2 = [[490, 520],
                          [900, 520],
                          [3850, 270]]
        for recorrido in posicionyellowgrunt2:
            yellowgrunt = YellowGrunt2(recorrido[0],recorrido[1])
            self.ListaYellowGrunt2.add(yellowgrunt) 

    def update(self):
        self.ListaYellowGrunt2.update()
     
    def draw(self, pantalla):
        self.ListaYellowGrunt2.draw(pantalla) 
#------------------------------------------------------------------------------------------------------------------------------------------------
class RedGrunt2(pygame.sprite.Sprite):
    def __init__(self, posX, posY):
        pygame.sprite.Sprite.__init__(self)
        self.RedGrunt1 = pygame.image.load("Gruntrojoder.png").convert_alpha()
        self.RedGrunt2 = pygame.image.load("Gruntrojo.png").convert_alpha()
        
        self.redgrunt1 = {}
        self.redgrunt1[0] = (0, 0, 70, 82)
        self.redgrunt1[1] = (70, 0, 60, 82)
        self.redgrunt1[2] = (130, 0, 60, 82)
        self.redgrunt1[3] = (190, 0, 70, 82)
        self.redgrunt1[4] = (260, 0, 70, 82)
        self.redgrunt1[5] = (330, 0, 70, 82)
        self.redgrunt1[6] = (400, 0, 70, 82)
        self.redgrunt1[7] = (470, 0, 80, 82)
        self.redgrunt1[8] = (550, 0, 84, 82)

        self.redgrunt2 = {}
        self.redgrunt2[0] = (570, 0, 64, 82)
        self.redgrunt2[1] = (510, 0, 60, 82)
        self.redgrunt2[2] = (444, 0, 66, 82)
        self.redgrunt2[3] = (370, 0, 74, 82)
        self.redgrunt2[4] = (300, 0, 70, 82)
        self.redgrunt2[5] = (240, 0, 60, 82)
        self.redgrunt2[6] = (170, 0, 70, 82)
        self.redgrunt2[7] = (90, 0, 80, 82)
        self.redgrunt2[8] = (0, 0, 90, 82)
        
        self.actualizacion = pygame.time.get_ticks()
        self.cual = 0     
        self.izquierda = False   
        self.obtenerDibujo()
        self.rect = self.image.get_rect()
        self.rect.topleft = (posX, posY)
        self.dx = 1
        self.PosicionX = posX

    def obtenerDibujo(self):
        if self.izquierda:
           self.image=self.RedGrunt2.subsurface(self.redgrunt2[self.cual])
        else:
           self.image=self.RedGrunt1.subsurface(self.redgrunt1[self.cual])

    def update(self):
        if self.actualizacion + 100 < pygame.time.get_ticks():
           self.cual += 1
           if self.cual > 8:
              self.cual = 0
           if self.cual == 4:
              disparoenemigo = True
           self.obtenerDibujo()
           self.actualizacion= pygame.time.get_ticks()
        
        TiempoMovimiento =pygame.time.get_ticks()/1000         
        t = TiempoMovimiento
        if t==2 or t==6 or t==10 or t==14 or t==18 or t==22 or t==26 or t==30 or t==34 or t==38 or t==42 or t==46 or t==50 or t==54 or t==58 or t==62 or t==66 or t==70 or t==74 or t==78 or t==82 or t==86 or t==90 or t==94 or t==98 or t==102 or t==106 or t==110 or t==114 or t==118 or t==122 or t==126 or t==130 or t==134 or t==138 or t==142 or t==146 or t==150 or t==154 or t==158 or t==162  or t==166 or t==170 or t==174 or t==178 or t==182 or t==186 or t==190 or t==194 or t==198 or t==202:
           self.izquierda = True

                
        if t==4 or t==8 or t==12 or t==16 or t==20 or t==24 or t==28 or t==32 or t==36 or t==40 or t==44 or t==48 or t==52 or t==56 or t==60 or t==64 or t==68 or t==72 or t==76 or t==80 or t==84 or t==88 or t==92 or t==96 or t==100 or t==104 or t==108 or t==112 or t==116 or t==120 or t==124 or t==128 or t==132 or t==136 or t==140 or t==144 or t==148 or t==152 or t==156 or t==160 or t==164 or t==168 or t==172 or t==176 or t==180 or t==184 or t==188 or t==192 or t==196 or t==200 or t==204:
           self.izquierda = False

        if self.izquierda == True:
           self.rect.move_ip(-self.dx,0)
        else:
           self.rect.move_ip(self.dx,0)

        if movimiento2 == True:
           if FondoDerecha2 == True:
              if personaje2.rect.x > 680:
                 self.rect.move_ip(0,0)
              else:
                 self.rect.move_ip(-VELOCIDAD,0)
           if FondoDerecha2 == False:
              if personaje2.rect.x < 680:
                 self.rect.move_ip(0,0)
              else:
                 self.rect.move_ip(VELOCIDAD,0)

class RedGruntNivel2(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.ListaRedGrunt2 = pygame.sprite.Group()

        posicionredgrunt2 = [[1530, 520],
                            [2000, 520],
                            [2670, 130],
                            [2400, 320],
                            [3050, 130],
                            [6700, 520],
                            [3560, 520],
                            [5920, 520],
                            [5420, 520]]
        for recorrido in posicionredgrunt2:
            redgrunt = RedGrunt2(recorrido[0],recorrido[1])
            self.ListaRedGrunt2.add(redgrunt) 

    def update(self):
        self.ListaRedGrunt2.update()
     
    def draw(self, pantalla):
        self.ListaRedGrunt2.draw(pantalla) 
#------------------------------------------------------------------------------------------------------------------------------------------------
class Elite2(pygame.sprite.Sprite):
    def __init__(self, posX, posY):
        pygame.sprite.Sprite.__init__(self)
        self.elite1 = pygame.image.load("Eliteder.png").convert_alpha()
        self.elite2 = pygame.image.load("Eliteizq.png").convert_alpha()
        
        self.Elite1 = {}
        self.Elite1[0] = (0, 0, 140, 127)
        self.Elite1[1] = (140, 0, 110, 127)
        self.Elite1[2] = (250, 0, 130, 127)
        self.Elite1[3] = (380, 0, 95, 127)
        self.Elite1[4] = (475, 0, 95, 127)
        self.Elite1[5] = (570, 0, 100, 127)
        self.Elite1[6] = (670, 0, 90, 127)
        self.Elite1[7] = (760, 0, 100, 127)
        self.Elite1[8] = (860, 0, 104, 127)

        self.Elite2 = {}
        self.Elite2[0] = (830, 0, 134, 127)
        self.Elite2[1] = (710, 0, 120, 127)
        self.Elite2[2] = (580, 0, 130, 127)
        self.Elite2[3] = (490, 0, 90, 127)
        self.Elite2[4] = (395, 0, 95, 127)
        self.Elite2[5] = (290, 0, 105, 127)
        self.Elite2[6] = (200, 0, 90, 127)
        self.Elite2[7] = (110, 0, 90, 127)
        self.Elite2[8] = (0, 0, 110, 127)
        
        self.actualizacion = pygame.time.get_ticks()
        self.cual = 0     
        self.izquierda = False   
        self.obtenerDibujo()
        self.rect = self.image.get_rect()
        self.rect.topleft = (posX, posY)
        self.dx = 1
        self.PosicionX = posX

    def obtenerDibujo(self):
        if self.izquierda:
            self.image=self.elite2.subsurface(self.Elite2[self.cual])
        else:
            self.image=self.elite1.subsurface(self.Elite1[self.cual])

    def update(self):
        if self.actualizacion + 100 < pygame.time.get_ticks():
           self.cual += 1
           if self.cual > 8:
              self.cual = 0
           self.obtenerDibujo()
           self.actualizacion= pygame.time.get_ticks()
        
        TiempoMovimiento =pygame.time.get_ticks()/1000         
        t = TiempoMovimiento
        if t==2 or t==6 or t==10 or t==14 or t==18 or t==22 or t==26 or t==30 or t==34 or t==38 or t==42 or t==46 or t==50 or t==54 or t==58 or t==62 or t==66 or t==70 or t==74 or t==78 or t==82 or t==86 or t==90 or t==94 or t==98 or t==102 or t==106 or t==110 or t==114 or t==118 or t==122 or t==126 or t==130 or t==134 or t==138 or t==142 or t==146 or t==150 or t==154 or t==158 or t==162  or t==166 or t==170 or t==174 or t==178 or t==182 or t==186 or t==190 or t==194 or t==198 or t==202:
           self.izquierda = True

                
        if t==4 or t==8 or t==12 or t==16 or t==20 or t==24 or t==28 or t==32 or t==36 or t==40 or t==44 or t==48 or t==52 or t==56 or t==60 or t==64 or t==68 or t==72 or t==76 or t==80 or t==84 or t==88 or t==92 or t==96 or t==100 or t==104 or t==108 or t==112 or t==116 or t==120 or t==124 or t==128 or t==132 or t==136 or t==140 or t==144 or t==148 or t==152 or t==156 or t==160 or t==164 or t==168 or t==172 or t==176 or t==180 or t==184 or t==188 or t==192 or t==196 or t==200 or t==204:
           self.izquierda = False

        if self.izquierda == True:
           self.rect.move_ip(-self.dx,0)
        else:
           self.rect.move_ip(self.dx,0)

        if movimiento2 == True:
           if FondoDerecha2 == True:
              if personaje2.rect.x > 680:
                 self.rect.move_ip(0,0)
              else:
                 self.rect.move_ip(-VELOCIDAD,0)
           if FondoDerecha2 == False:
              if personaje2.rect.x < 680:
                 self.rect.move_ip(0,0)
              else:
                 self.rect.move_ip(VELOCIDAD,0)

class EliteNivel2(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.ListaElite2 = pygame.sprite.Group()

        posicionelite2 = [[3010, 480],
                          [3365, 90],
                          [3700, 480],
                          [5520, 480],
                          [6200, 480],
                          [5420, 108],
                          [6650, 130],
                          [7500, 480],
                          [4500, 480]]
        for recorrido in posicionelite2:
            elite = Elite2(recorrido[0],recorrido[1])
            self.ListaElite2.add(elite) 

    def update(self):
        self.ListaElite2.update()
     
    def draw(self, pantalla):
        self.ListaElite2.draw(pantalla) 
#------------------------------------------------------------------------------------------------------------------------------------------------
class JackalMayor(pygame.sprite.Sprite):
    def __init__(self, posX, posY):
        pygame.sprite.Sprite.__init__(self)
        self.jackalmayor1 = pygame.image.load("JackalMayorDer.png").convert_alpha()
        self.jackalmayor2 = pygame.image.load("JackalMayor.png").convert_alpha()
        
        self.JackalMayor1 = {}
        self.JackalMayor1[0] = (0, 0, 92, 95)
        self.JackalMayor1[1] = (92, 0, 90, 95)
        self.JackalMayor1[2] = (182, 0, 98, 95)
        self.JackalMayor1[3] = (280, 0, 100, 95)
        self.JackalMayor1[4] = (380, 0, 90, 95)
        self.JackalMayor1[5] = (470, 0, 95, 95)
        self.JackalMayor1[6] = (565, 0, 95, 95)

        self.JackalMayor2 = {}
        self.JackalMayor2[0] = (560, 0, 100, 95)
        self.JackalMayor2[1] = (475, 0, 85, 95)
        self.JackalMayor2[2] = (380, 0, 95, 95)
        self.JackalMayor2[3] = (280, 0, 100, 95)
        self.JackalMayor2[4] = (190, 0, 90, 95)
        self.JackalMayor2[5] = (90, 0, 100, 95)
        self.JackalMayor2[6] = (0, 0, 90, 95)
        
        self.actualizacion = pygame.time.get_ticks()
        self.cual = 0     
        self.izquierda = False   
        self.obtenerDibujo()
        self.rect = self.image.get_rect()
        self.rect.topleft = (posX, posY)
        self.dx = 1
        self.PosicionX = posX

    def obtenerDibujo(self):
        if self.izquierda:
            self.image=self.jackalmayor2.subsurface(self.JackalMayor2[self.cual])
        else:
            self.image=self.jackalmayor1.subsurface(self.JackalMayor1[self.cual])

    def update(self):
        if self.actualizacion + 100 < pygame.time.get_ticks():
           self.cual += 1
           if self.cual > 6:
              self.cual = 0
           self.obtenerDibujo()
           self.actualizacion= pygame.time.get_ticks()
        
        TiempoMovimiento =pygame.time.get_ticks()/1000         
        t = TiempoMovimiento
        if t==2 or t==6 or t==10 or t==14 or t==18 or t==22 or t==26 or t==30 or t==34 or t==38 or t==42 or t==46 or t==50 or t==54 or t==58 or t==62 or t==66 or t==70 or t==74 or t==78 or t==82 or t==86 or t==90 or t==94 or t==98 or t==102 or t==106 or t==110 or t==114 or t==118 or t==122 or t==126 or t==130 or t==134 or t==138 or t==142 or t==146 or t==150 or t==154 or t==158 or t==162  or t==166 or t==170 or t==174 or t==178 or t==182 or t==186 or t==190 or t==194 or t==198 or t==202:
           self.izquierda = True

                
        if t==4 or t==8 or t==12 or t==16 or t==20 or t==24 or t==28 or t==32 or t==36 or t==40 or t==44 or t==48 or t==52 or t==56 or t==60 or t==64 or t==68 or t==72 or t==76 or t==80 or t==84 or t==88 or t==92 or t==96 or t==100 or t==104 or t==108 or t==112 or t==116 or t==120 or t==124 or t==128 or t==132 or t==136 or t==140 or t==144 or t==148 or t==152 or t==156 or t==160 or t==164 or t==168 or t==172 or t==176 or t==180 or t==184 or t==188 or t==192 or t==196 or t==200 or t==204:
           self.izquierda = False

        if self.izquierda == True:
           self.rect.move_ip(-self.dx,0)
        else:
           self.rect.move_ip(self.dx,0)

        if movimiento2 == True:
           if FondoDerecha2 == True:
              if personaje2.rect.x > 680:
                 self.rect.move_ip(0,0)
              else:
                 self.rect.move_ip(-VELOCIDAD,0)
           if FondoDerecha2 == False:
              if personaje2.rect.x < 680:
                 self.rect.move_ip(0,0)
              else:
                 self.rect.move_ip(VELOCIDAD,0)

class JackalMayorNivel1(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.ListaJackalMayor = pygame.sprite.Group()

        posicionjackal = [[510, 518],
                          [1780, 518],
                          [3210, 518],
                          [7370, 170],
                          [1260, 518]]

        for recorrido in posicionjackal:
            jackal = JackalMayor(recorrido[0],recorrido[1])
            self.ListaJackalMayor.add(jackal) 

    def update(self):
        self.ListaJackalMayor.update()
     
    def draw(self, pantalla):
        self.ListaJackalMayor.draw(pantalla) 
#------------------------------------------------------------------------------------------------------------------------------------------------
class Hunter(pygame.sprite.Sprite):
    def __init__(self, posX, posY):
        pygame.sprite.Sprite.__init__(self)
        self.Hunter1 = pygame.image.load("HunterDer.png").convert_alpha()
        self.Hunter2 = pygame.image.load("Hunter.png").convert_alpha()
        
        self.hunter1 = {}
        self.hunter1[0] = (0, 0, 170, 151)
        self.hunter1[1] = (170, 0, 120, 151)
        self.hunter1[2] = (290, 0, 150, 151)
        self.hunter1[3] = (440, 0, 150, 151)
        self.hunter1[4] = (590, 0, 130, 151)
        self.hunter1[5] = (720, 0, 140, 151)
        self.hunter1[6] = (860, 0, 150, 151)
        self.hunter1[7] = (1010, 0, 130, 151)
        self.hunter1[8] = (1140, 0, 125, 151)

        self.hunter2 = {}
        self.hunter2[0] = (1090, 0, 175, 151)
        self.hunter2[1] = (960, 0, 130, 151)
        self.hunter2[2] = (820, 0, 140, 151)
        self.hunter2[3] = (670, 0, 150, 151)
        self.hunter2[4] = (540, 0, 130, 151)
        self.hunter2[5] = (406, 0, 134, 151)
        self.hunter2[6] = (250, 0, 156, 151)
        self.hunter2[7] = (120, 0, 130, 151)
        self.hunter2[8] = (0, 0, 120, 151)
        
        self.actualizacion = pygame.time.get_ticks()
        self.cual = 0     
        self.izquierda = False   
        self.obtenerDibujo()
        self.rect = self.image.get_rect()
        self.rect.topleft = (posX, posY)
        self.dx = 1
        self.PosicionX = posX

    def obtenerDibujo(self):
        if self.izquierda:
           self.image=self.Hunter2.subsurface(self.hunter2[self.cual])
        else:
           self.image=self.Hunter1.subsurface(self.hunter1[self.cual])

    def update(self):
        if self.actualizacion + 100 < pygame.time.get_ticks():
           self.cual += 1
           if self.cual > 8:
              self.cual = 0
           self.obtenerDibujo()
           self.actualizacion= pygame.time.get_ticks()
        
        TiempoMovimiento =pygame.time.get_ticks()/1000         
        t = TiempoMovimiento
        if t==2 or t==6 or t==10 or t==14 or t==18 or t==22 or t==26 or t==30 or t==34 or t==38 or t==42 or t==46 or t==50 or t==54 or t==58 or t==62 or t==66 or t==70 or t==74 or t==78 or t==82 or t==86 or t==90 or t==94 or t==98 or t==102 or t==106 or t==110 or t==114 or t==118 or t==122 or t==126 or t==130 or t==134 or t==138 or t==142 or t==146 or t==150 or t==154 or t==158 or t==162  or t==166 or t==170 or t==174 or t==178 or t==182 or t==186 or t==190 or t==194 or t==198 or t==202:
           self.izquierda = True

                
        if t==4 or t==8 or t==12 or t==16 or t==20 or t==24 or t==28 or t==32 or t==36 or t==40 or t==44 or t==48 or t==52 or t==56 or t==60 or t==64 or t==68 or t==72 or t==76 or t==80 or t==84 or t==88 or t==92 or t==96 or t==100 or t==104 or t==108 or t==112 or t==116 or t==120 or t==124 or t==128 or t==132 or t==136 or t==140 or t==144 or t==148 or t==152 or t==156 or t==160 or t==164 or t==168 or t==172 or t==176 or t==180 or t==184 or t==188 or t==192 or t==196 or t==200 or t==204:
           self.izquierda = False

        if self.izquierda == True:
           self.rect.move_ip(-self.dx,0)
        else:
           self.rect.move_ip(self.dx,0)

        if movimiento2 == True:
           if FondoDerecha2 == True:
              if personaje2.rect.x > 680:
                 self.rect.move_ip(0,0)
              else:
                 self.rect.move_ip(-VELOCIDAD,0)
           if FondoDerecha2 == False:
              if personaje2.rect.x < 680:
                 self.rect.move_ip(0,0)
              else:
                 self.rect.move_ip(VELOCIDAD,0)

class HunterNivel1(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.ListaHunter = pygame.sprite.Group()

        posicionhunter = [[990, 250],
                            [1845, 450],
                            [2700, 450],
                            [4110, 50],
                            [3910, 450],
                            [5200, 450]]
        for recorrido in posicionhunter:
            hunter = Hunter(recorrido[0],recorrido[1])
            self.ListaHunter.add(hunter) 

    def update(self):
        self.ListaHunter.update()
     
    def draw(self, pantalla):
        self.ListaHunter.draw(pantalla) 
#--------------------------------------------------------------------------------------------------------------------------------------------------
class Brute(pygame.sprite.Sprite):
    def __init__(self, posX, posY):
        pygame.sprite.Sprite.__init__(self)
        self.Brute1 = pygame.image.load("BruteDer.png").convert_alpha()
        self.Brute2 = pygame.image.load("Brute.png").convert_alpha()

        self.brute1 = {}
        self.brute1[0] = (0, 0, 130, 167)
        self.brute1[1] = (130, 0, 160, 167)
        self.brute1[2] = (290, 0, 140, 167)
        self.brute1[3] = (430, 0, 123, 167)
        self.brute1[4] = (553, 0, 131, 167)
        self.brute1[5] = (684, 0, 109, 167)

        self.brute2 = {}
        self.brute2[0] = (670, 0, 123, 167)
        self.brute2[1] = (510, 0, 160, 167)
        self.brute2[2] = (360, 0, 150, 167)
        self.brute2[3] = (238, 0, 122, 167)
        self.brute2[4] = (110, 0, 128, 167)
        self.brute2[5] = (0, 0, 110, 167)
        
        self.actualizacion = pygame.time.get_ticks()
        self.cual = 0     
        self.izquierda = False   
        self.obtenerDibujo()
        self.rect = self.image.get_rect()
        self.rect.topleft = (posX, posY)
        self.dx = 1
        self.PosicionX = posX

    def obtenerDibujo(self):
        if self.izquierda:
            self.image=self.Brute2.subsurface(self.brute2[self.cual])
        else:
            self.image=self.Brute1.subsurface(self.brute1[self.cual])

    def update(self):
        if self.actualizacion + 100 < pygame.time.get_ticks():
           self.cual += 1
           if self.cual > 5:
              self.cual = 0
           self.obtenerDibujo()
           self.actualizacion= pygame.time.get_ticks()
        
        TiempoMovimiento =pygame.time.get_ticks()/1000         
        t = TiempoMovimiento
        if t==2 or t==6 or t==10 or t==14 or t==18 or t==22 or t==26 or t==30 or t==34 or t==38 or t==42 or t==46 or t==50 or t==54 or t==58 or t==62 or t==66 or t==70 or t==74 or t==78 or t==82 or t==86 or t==90 or t==94 or t==98 or t==102 or t==106 or t==110 or t==114 or t==118 or t==122 or t==126 or t==130 or t==134 or t==138 or t==142 or t==146 or t==150 or t==154 or t==158 or t==162  or t==166 or t==170 or t==174 or t==178 or t==182 or t==186 or t==190 or t==194 or t==198 or t==202:
           self.izquierda = True

                
        if t==4 or t==8 or t==12 or t==16 or t==20 or t==24 or t==28 or t==32 or t==36 or t==40 or t==44 or t==48 or t==52 or t==56 or t==60 or t==64 or t==68 or t==72 or t==76 or t==80 or t==84 or t==88 or t==92 or t==96 or t==100 or t==104 or t==108 or t==112 or t==116 or t==120 or t==124 or t==128 or t==132 or t==136 or t==140 or t==144 or t==148 or t==152 or t==156 or t==160 or t==164 or t==168 or t==172 or t==176 or t==180 or t==184 or t==188 or t==192 or t==196 or t==200 or t==204:
           self.izquierda = False

        if self.izquierda == True:
           self.rect.move_ip(-self.dx,0)
        else:
           self.rect.move_ip(self.dx,0)

        if movimiento2 == True:
           if FondoDerecha2 == True:
              if personaje2.rect.x > 680:
                 self.rect.move_ip(0,0)
              else:
                 self.rect.move_ip(-VELOCIDAD,0)
           if FondoDerecha2 == False:
              if personaje2.rect.x < 680:
                 self.rect.move_ip(0,0)
              else:
                 self.rect.move_ip(VELOCIDAD,0)

class BruteNivel1(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.ListaBrute = pygame.sprite.Group()

        posicionbrute = [[2390, 435],
                          [3350, 435],
                          [4700, 435],
                          [4060, 435],
                          [6980, 100],
                          [6180, 100],
                          [6920, 435],
                          [7450, 435],
                          [5840, 180]]
        for recorrido in posicionbrute:
            brute = Brute(recorrido[0],recorrido[1])
            self.ListaBrute.add(brute) 

    def update(self):
        self.ListaBrute.update()
     
    def draw(self, pantalla):
        self.ListaBrute.draw(pantalla) 
#-----------------------------------------------------------------------------------------------------------------------------------------------------
#Modificadores Nivel 1
#-----------------------------------------------------------------------------------------------------------------------------------------------------
class Vidas(pygame.sprite.Sprite):
    def __init__(self, coordenadas, imagen):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("botiquin.png")
        self.rect = self.image.get_rect()
        self.rect.center = coordenadas
        self.actualizacion = pygame.time.get_ticks()
        self.maximo = self.rect.bottom+5
        self.minimo = self.rect.top-5
        self.dy = 1

    def update(self):
        if self.actualizacion + 40 < pygame.time.get_ticks():
           self.rect.move_ip(0,self.dy)
           if self.rect.bottom > self.maximo or self.rect.top < self.minimo:
              self.dy = -self.dy
           self.actualizacion= pygame.time.get_ticks()

        if scroll:
           if FondoDerecha == True:
              if personaje.rect.x > 680:
                 self.rect.move_ip(0,0)
              else:
                 self.rect.move_ip(-VELOCIDAD,0)
           if FondoDerecha == False:
              if personaje.rect.x < 680:
                 self.rect.move_ip(0,0)
              else:
                 self.rect.move_ip(VELOCIDAD,0)

class VidasNivel1(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.ListaVidas = pygame.sprite.Group()
        self.Vida = pygame.image.load("botiquin.png")
        self.transparente = self.Vida.get_at((0,0))
        self.Vida.set_colorkey(self.transparente)
        posicionvida = [[1270, 100],
                        [7770, 510],
                        [5740, 490]]
        for recorrido in posicionvida:
            vida = Vidas((recorrido[0],recorrido[1]), self.Vida)
            self.ListaVidas.add(vida) 

    def update(self):
        self.ListaVidas.update()
     
    def draw(self, pantalla):
        self.ListaVidas.draw(pantalla) 
#------------------------------------------------------------------------------------------------------------------------------------------------
class Balas(pygame.sprite.Sprite):
    def __init__(self, coordenadas, imagen):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("Halogun.png")
        self.rect = self.image.get_rect()
        self.rect.center = coordenadas
        self.actualizacion = pygame.time.get_ticks()
        self.maximo = self.rect.bottom+5
        self.minimo = self.rect.top-5
        self.dy = 1

    def update(self):
        if self.actualizacion + 40 < pygame.time.get_ticks():
           self.rect.move_ip(0,self.dy)
           if self.rect.bottom > self.maximo or self.rect.top < self.minimo:
              self.dy = -self.dy
           self.actualizacion= pygame.time.get_ticks()

        if scroll:
           if FondoDerecha == True:
              if personaje.rect.x > 680:
                 self.rect.move_ip(0,0)
              else:
                 self.rect.move_ip(-VELOCIDAD,0)
           if FondoDerecha == False:
              if personaje.rect.x < 680:
                 self.rect.move_ip(0,0)
              else:
                 self.rect.move_ip(VELOCIDAD,0)

class BalasNivel1(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.ListaBalas = pygame.sprite.Group()
        self.Bala = pygame.image.load("Halogun.png")
        self.transparente = self.Bala.get_at((0,0))
        self.Bala.set_colorkey(self.transparente)
        posicionbala = [[1890, 250],
                        [7870, 490],
                        [2490, 510]]
        for recorrido in posicionbala:
            bala = Balas((recorrido[0],recorrido[1]), self.Bala)
            self.ListaBalas.add(bala) 

    def update(self):
        self.ListaBalas.update()
     
    def draw(self, pantalla):
        self.ListaBalas.draw(pantalla) 
#------------------------------------------------------------------------------------------------------------------------------------------------
class Meta(pygame.sprite.Sprite):
    def __init__(self, coordenadas, imagen):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("pozometa.png")
        self.rect = self.image.get_rect()
        self.rect.center = coordenadas
        self.actualizacion = pygame.time.get_ticks()
        self.maximo = self.rect.bottom+5
        self.minimo = self.rect.top-5
        self.dy = 1

    def update(self):
        if self.actualizacion + 40 < pygame.time.get_ticks():
          # self.rect.move_ip(0,self.dy)
           if self.rect.bottom > self.maximo or self.rect.top < self.minimo:
              self.dy = -self.dy
           self.actualizacion= pygame.time.get_ticks()

        if scroll:
           if FondoDerecha == True:
              if personaje.rect.x > 680:
                 self.rect.move_ip(0,0)
              else:
                 self.rect.move_ip(-VELOCIDAD,0)
           if FondoDerecha == False:
              if personaje.rect.x < 680:
                 self.rect.move_ip(0,0)
              else:
                 self.rect.move_ip(VELOCIDAD,0)

class MetaNivel1(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.ListaMeta = pygame.sprite.Group()
        self.Meta = pygame.image.load("pozometa.png")
        self.transparente = self.Meta.get_at((0,0))
        self.Meta.set_colorkey(self.transparente)
        posicionmeta = [[8115, 510]]
        for recorrido in posicionmeta:
            meta = Meta((recorrido[0],recorrido[1]), self.Meta)
            self.ListaMeta.add(meta) 

    def update(self):
        self.ListaMeta.update()
     
    def draw(self, pantalla):
        self.ListaMeta.draw(pantalla) 
#------------------------------------------------------------------------------------------------------------------------------------------------
#Modificadores nivel 2
#------------------------------------------------------------------------------------------------------------------------------------------------
class Vidas2(pygame.sprite.Sprite):
    def __init__(self, coordenadas, imagen):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("botiquin2.png")
        self.rect = self.image.get_rect()
        self.rect.center = coordenadas
        self.actualizacion = pygame.time.get_ticks()
        self.maximo = self.rect.bottom+5
        self.minimo = self.rect.top-5
        self.dy = 1

    def update(self):
        if self.actualizacion + 40 < pygame.time.get_ticks():
           self.rect.move_ip(0,self.dy)
           if self.rect.bottom > self.maximo or self.rect.top < self.minimo:
              self.dy = -self.dy
           self.actualizacion= pygame.time.get_ticks()

        if movimiento2 == True:
           if FondoDerecha2 == True:
              if personaje2.rect.x > 680:
                 self.rect.move_ip(0,0)
              else:
                 self.rect.move_ip(-VELOCIDAD,0)
           if FondoDerecha2 == False:
              if personaje2.rect.x < 680:
                 self.rect.move_ip(0,0)
              else:
                 self.rect.move_ip(VELOCIDAD,0)

class VidasNivel2(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.ListaVidas2 = pygame.sprite.Group()
        self.Vida = pygame.image.load("botiquin2.png")
        self.transparente = self.Vida.get_at((0,0))
        self.Vida.set_colorkey(self.transparente)
        posicionvida2 = [[5100, 210],
                         [4560, 210]]
        for recorrido in posicionvida2:
            vida2 = Vidas2((recorrido[0],recorrido[1]), self.Vida)
            self.ListaVidas2.add(vida2) 

    def update(self):
        self.ListaVidas2.update()
     
    def draw(self, pantalla):
        self.ListaVidas2.draw(pantalla) 
#------------------------------------------------------------------------------------------------------------------------------------------------
class Balas2(pygame.sprite.Sprite):
    def __init__(self, coordenadas, imagen):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("Halogun.png")
        self.rect = self.image.get_rect()
        self.rect.center = coordenadas
        self.actualizacion = pygame.time.get_ticks()
        self.maximo = self.rect.bottom+5
        self.minimo = self.rect.top-5
        self.dy = 1

    def update(self):
        if self.actualizacion + 40 < pygame.time.get_ticks():
           self.rect.move_ip(0,self.dy)
           if self.rect.bottom > self.maximo or self.rect.top < self.minimo:
              self.dy = -self.dy
           self.actualizacion= pygame.time.get_ticks()

        if movimiento2 == True:
           if FondoDerecha2 == True:
              if personaje2.rect.x > 680:
                 self.rect.move_ip(0,0)
              else:
                 self.rect.move_ip(-VELOCIDAD,0)
           if FondoDerecha2 == False:
              if personaje2.rect.x < 680:
                 self.rect.move_ip(0,0)
              else:
                 self.rect.move_ip(VELOCIDAD,0)

class BalasNivel2(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.ListaBalas = pygame.sprite.Group()
        self.Bala = pygame.image.load("Halogun.png")
        self.transparente = self.Bala.get_at((0,0))
        self.Bala.set_colorkey(self.transparente)
        posicionbala = [[1090, 100],
                        [2930, 80]]
        for recorrido in posicionbala:
            bala = Balas2((recorrido[0],recorrido[1]), self.Bala)
            self.ListaBalas.add(bala) 

    def update(self):
        self.ListaBalas.update()
     
    def draw(self, pantalla):
        self.ListaBalas.draw(pantalla)
#------------------------------------------------------------------------------------------------------------------------------------------------
class Meta2(pygame.sprite.Sprite):
    def __init__(self, coordenadas, imagen):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("portal.png")
        self.rect = self.image.get_rect()
        self.rect.center = coordenadas
        self.actualizacion = pygame.time.get_ticks()
        self.maximo = self.rect.bottom+5
        self.minimo = self.rect.top-5
        self.dy = 1

    def update(self):
        if self.actualizacion + 40 < pygame.time.get_ticks():
          # self.rect.move_ip(0,self.dy)
           if self.rect.bottom > self.maximo or self.rect.top < self.minimo:
              self.dy = -self.dy
           self.actualizacion= pygame.time.get_ticks()

        if movimiento2 == True:
           if FondoDerecha2 == True:
              if personaje2.rect.x > 680:
                 self.rect.move_ip(0,0)
              else:
                 self.rect.move_ip(-VELOCIDAD,0)
           if FondoDerecha2 == False:
              if personaje2.rect.x < 680:
                 self.rect.move_ip(0,0)
              else:
                 self.rect.move_ip(VELOCIDAD,0)

class MetaNivel2(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.ListaMeta = pygame.sprite.Group()
        self.Meta = pygame.image.load("portal.png")
        self.transparente = self.Meta.get_at((0,0))
        self.Meta.set_colorkey(self.transparente)
        posicionmeta = [[7700, 510]]
        for recorrido in posicionmeta:
            meta = Meta2((recorrido[0],recorrido[1]), self.Meta)
            self.ListaMeta.add(meta) 

    def update(self):
        self.ListaMeta.update()
     
    def draw(self, pantalla):
        self.ListaMeta.draw(pantalla) 
#------------------------------------------------------------------------------------------------------------------------------------------------
class Sounds():
    def __init__(self):
       self.EnterMenu = pygame.mixer.Sound(os.path.join("EnterMenu.wav"))
       self.EnterMenu.set_volume(1)
       self.Pausa = pygame.mixer.Sound(os.path.join("Pausa.wav"))
       self.Pausa.set_volume(1)
       self.Salto = pygame.mixer.Sound(os.path.join("Saltar.wav"))
       self.Salto.set_volume(0.2)
       self.Halo_headgun = pygame.mixer.Sound(os.path.join("Halo_gun.wav"))
       self.Halo_headgun.set_volume(0.8)
       self.Destruido = pygame.mixer.Sound(os.path.join("devildying.wav"))
       self.Destruido.set_volume(1)
       self.death = pygame.mixer.Sound(os.path.join("death.wav"))
       self.death.set_volume(1)
       self.GameOver = pygame.mixer.Sound(os.path.join("GameOver.wav"))
       self.GameOver.set_volume(1)
       self.MasVida = pygame.mixer.Sound(os.path.join("Halovida.wav"))
       self.MasVida.set_volume(1)
       self.MasBala = pygame.mixer.Sound(os.path.join("Balas.wav"))
       self.MasBala.set_volume(1)
       self.Meta = pygame.mixer.Sound(os.path.join("One_Final_Effort.wav"))
       self.Meta.set_volume(1)
#------------------------------------------------------------------------------------------------------------------------------------------------
#INICIALIZACION DE VARIABLES
pygame.init()
pygame.mixer.init()
#------------------------------------------------------------------------------------------------------------------------------------------------
#COLORES
blanco = (255,255,255)
negro = (0,0,0)
amarillo = (255,255,0)
azul = (0,0,255)
#------------------------------------------------------------------------------------------------------------------------------------------------
#DIMENSIONES DE LA VENTANA
pantalla = pygame.display.set_mode((ANCHO,ALTO),pygame.FULLSCREEN)
pygame.display.set_caption(" HALO ")
#------------------------------------------------------------------------------------------------------------------------------------------------
#DIMENSIONES DEL MENU
MenuX = 410
MenuY = 478
DimensionMenu = [MenuX,MenuY]
#------------------------------------------------------------------------------------------------------------------------------------------------
#DIMENSIONES DEL MENU DE PAUSA
MenuPausaX = 410
MenuPausaY = 478
DimensionMenuPausa = [MenuPausaX,MenuPausaY]
#------------------------------------------------------------------------------------------------------------------------------------------------
#IMAGENES Y MUSICA DEL MENU
Seleccion = pygame.image.load('halo1.ico').convert_alpha()
pygame.mixer.music.load('Musicafondo.mp3')
pygame.mixer.music.play(-1)
#------------------------------------------------------------------------------------------------------------------------------------------------
#MUSICA Y SONIDOS
sounds = Sounds()
#------------------------------------------------------------------------------------------------------------------------------------------------
#PERSONAJE
personaje = Personaje()
personaje2 = Personaje2()

fondo2 = FondoAnimado2(0,0)
#------------------------------------------------------------------------------------------------------------------------------------------------
#TIPOS DE FUENTES TEXTOS
FuenteEstadisticas = pygame.font.Font('Halo3.ttf', 20)
FuenteGameOver = pygame.font.Font('Halo3.ttf', 60)
FuenteMisionCompleta = pygame.font.Font('Halo3.ttf', 40)
FuentePresioneEspacio = pygame.font.Font('Halo3.ttf', 30)
FuentePuntaje = pygame.font.Font('Halo3.ttf', 3)
#------------------------------------------------------------------------------------------------------------------------------------------------
#VARIABLES DE JUEGO
salir = False
scroll = False
movimiento2 = False
FondoDerecha = False
FondoDerecha2 = False
reloj = pygame.time.Clock() 
textoTiempo = TextoTiempo()
EliminarDisparo = False
ReiniciarTiempo = False 
CambioNivel2 = False
disparoenemigo = False
Puntaje = 0
CantidadVidas = 5
CantidadBalas = 12
BASE_PERSONAJE = 600
#------------------------------------------------------------------------------------------------------------------------------------------------
# ESTRUCTURA DEL TEXTO DEL MENU 
def TextoMenu(texto, posx, posy, negro):
    fuente = pygame.font.Font("Halo3.ttf", 35)
    salida = pygame.font.Font.render(fuente, texto, 0, negro)
    salida_rect = salida.get_rect()
    salida_rect.centerx = posx
    salida_rect.centery = posy
    return salida, salida_rect
#------------------------------------------------------------------------------------------------------------------------------------------------
# ESTRUCTURA DEL TEXTO DEL MENU DE PAUSA
def TextoMenuPausa(texto, posx, posy, negro):
    fuente = pygame.font.Font("Halo3.ttf", 40)
    salida = pygame.font.Font.render(fuente, texto, 0, negro)
    salida_rect = salida.get_rect()
    salida_rect.centerx = posx
    salida_rect.centery = posy
    return salida, salida_rect
#------------------------------------------------------------------------------------------------------------------------------------------------
pos5 = -350
tiempo5 = 0
def MovimientoTitulo():
   global pos5, tiempo5
   pos5 = pos5 + 5
   if pos5 > 500:
      pos5 = 500
#------------------------------------------------------------------------------------------------------------------------------------------------
pos6 = -500
tiempo6 = 0
def MovimientoGameOver():
   global pos6, tiempo6
   pos6 = pos6 + 3
   if pos6 > 500:
      pos6 = 500
#------------------------------------------------------------------------------------------------------------------------------------------------
pos7 = -350
tiempo7 = 0
def MovimientoNivel1Completo():
   global pos7, tiempo7
   pos7 = pos7 + 2
   if pos7 > 250:
      pos7 = 250
#------------------------------------------------------------------------------------------------------------------------------------------------
pos8 = 1000
def MovimientoLogoUniversidad():
   global pos8
   pos8 = pos8 - 4
   if pos8 < 250:
      pos8 = 250
#------------------------------------------------------------------------------------------------------------------------------------------------
pos9 = 2200
def MovimientoComputador():
   global pos9
   pos9 = pos9 - 4
   if pos9 < 600:
      pos9 = 600
#------------------------------------------------------------------------------------------------------------------------------------------------
pos11 = 1900
def MovimientoNombre1():
   global pos11
   pos11 = pos11 - 2
   if pos11 < 660:
      pos11 = 660
#------------------------------------------------------------------------------------------------------------------------------------------------
pos12 = 2000
def MovimientoNombre2():
   global pos12
   pos12 = pos12 - 2
   if pos12 < 710:
      pos12 = 710
#------------------------------------------------------------------------------------------------------------------------------------------------
pos13 = -200
def MovimientoMision1Completa():
   global pos13
   pos13 = pos13 + 2
   if pos13 > 485:
      pos13 = 485
#------------------------------------------------------------------------------------------------------------------------------------------------
pos14 = 1400
def MovimientoPresioneEspacioMeta():
   global pos14
   pos14 = pos14 - 2
   if pos14 < 430:
      pos14 = 430
#------------------------------------------------------------------------------------------------------------------------------------------------
pos15 = 1400
def MovimientoPresioneEspacioGameOver():
   global pos15
   pos15 = pos15 - 2
   if pos15 < 400:
      pos15 = 400
#------------------------------------------------------------------------------------------------------------------------------------------------
#################################################### FUNCION PRINCIPAL DE INICIO DEL JUEGO #################################################### 
#------------------------------------------------------------------------------------------------------------------------------------------------
def IniciarJuego():
 
    #IMAGEN DE FONDO NIVEL 1
    FondoAnimado1 = FondoAnimado(0,0)
    FondoAnimadoGrupo = pygame.sprite.RenderUpdates(FondoAnimado1)
    #CREACION DE PLATAFORMAS NIVEL 1
    GrupoPlataformas = []
    GrupoPlataformas.append(PlataformasNivel1())
    DibujoPlataformas = GrupoPlataformas[0]
    personaje.nivel = DibujoPlataformas

    #CREACION DE GRUNT AMARRILLO
    GrupoYellowGrunt = []
    GrupoYellowGrunt.append(YellowGruntNivel1())
    DibujoYellowGrunt = GrupoYellowGrunt[0]
    personaje.posicionyellowgrunt = DibujoYellowGrunt
    #CREACION DE GRUNT ROJO
    GrupoRedGrunt = []
    GrupoRedGrunt.append(RedGruntNivel1())
    DibujoRedGrunt = GrupoRedGrunt[0]
    personaje.posicionredgrunt = DibujoRedGrunt
    #CREACION DE ELITE
    GrupoElite = []
    GrupoElite.append(EliteNivel1())
    DibujoElite = GrupoElite[0]
    personaje.posicionelite = DibujoElite
    #CREACION DE MODIFICADOR VIDAS
    GrupoVidas = []
    GrupoVidas.append(VidasNivel1())
    DibujoVidas = GrupoVidas[0]
    personaje.posicionvida = DibujoVidas
    #CREACION DE MODIFICADOR BALAS
    GrupoBalas = []
    GrupoBalas.append(BalasNivel1())
    DibujoBalas = GrupoBalas[0]
    personaje.posicionbala = DibujoBalas
    #CREACION DE META
    GrupoMeta = []
    GrupoMeta.append(MetaNivel1())
    DibujoMeta = GrupoMeta[0]
    personaje.posicionmeta = DibujoMeta
    #ICONOS DE OBJETOS
    IconoVidas = pygame.image.load('botiquin.png').convert_alpha()
    IconoBalas = pygame.image.load('Halogun.png').convert_alpha()
    #PERSONAJE
    PersonajeGrupo = pygame.sprite.RenderUpdates(personaje)
    personaje.rect.x = 50
    personaje.rect.y = BASE_PERSONAJE
    ListaSpritesActivos = pygame.sprite.Group()
    ListaSpritesActivos.add(personaje)
    #DISPAROS
    DisparosGrupo = pygame.sprite.RenderUpdates()
    DisparosGrupo2 = pygame.sprite.RenderUpdates()
#------------------------------------------------------------------------------------------------------------------------------------------------
    pygame.event.clear
    os.system('clear')
    salir = False
    FinGameOver = False
    FinMeta = False
    pygame.mixer.music.stop()
    pygame.mixer.music.load('Fondohalo.mp3')
    pygame.mixer.music.play(-1)

    FondoGameOver = pygame.image.load('FondoMenuPausa.png').convert_alpha() 
    Elite = pygame.image.load('Elite.png').convert_alpha()
    Halodied = pygame.image.load('halodied.png').convert_alpha()
    FondoMensajeMeta = pygame.image.load('FondoMenuPausa.png').convert_alpha() 
    Halo3MC = pygame.image.load('Halo3MC.png').convert_alpha() 
    MensajeHalo = pygame.image.load('Halo.png').convert_alpha() 

    TextoGameOver = FuenteGameOver.render("GAME OVER", 1, (azul))
    TextoMision1Completa = FuenteMisionCompleta.render("MISION COMPLETA", 1, (blanco))
    TextoPresioneEspacioMeta = FuentePresioneEspacio.render("PRESIONE ENTER PARA CONTINUAR", 1, (amarillo))
    TextoPresioneEspacioGameOver = FuentePresioneEspacio.render("PRESIONE ESPACIO PARA CONTINUAR", 1, (azul))

    Mas100Puntos = FuentePuntaje.render("+100", 1, (negro))

    global event, scroll, FondoDerecha, EliminarDisparo, MenuPausaY, DimensionMenuPausa, Puntaje
    global centSeg, unidSeg, deceSeg, unidMin, deceMin, PausaTiempo, CambioNivel2, CantidadVidas, CantidadBalas
    while salir != True: 
       reloj.tick(60) 
       tecla = pygame.key.get_pressed()
       for event in pygame.event.get():   
           if event.type == pygame.QUIT:
              salir = True
           if tecla[pygame.K_s]:
              sys.exit()
           if tecla[pygame.K_SPACE]:
                print "Disparar"
                personaje.cual = 2
                scroll = False
                if CantidadBalas == 0 or CantidadVidas == 0 or FinMeta == True:
                   CantidadBalas = CantidadBalas
                else:
                   sounds.Halo_headgun.play()
                   CantidadBalas -= 1
                   if personaje.izquierda == True:
                      DisparosGrupo.add(DisparoIzquierda(personaje.rect.left-10, personaje.rect.y+40))
                   if personaje.izquierda == False:
                      DisparosGrupo.add(DisparoDerecha(personaje.rect.right-10, personaje.rect.y+40))
#------------------------------------------------------------------------------------------------------------------------------------------------   
       if event.type == pygame.KEYDOWN:

          if tecla[pygame.K_RIGHT]:
             personaje.izquierda = False
             FondoDerecha = True
             if CantidadVidas == 0 or FinMeta == True:
                  scroll = False
             else:
                if pygame.time.get_ticks()-personaje.tiempo > personaje.cuanto:
                   personaje.tiempo = pygame.time.get_ticks()
                   personaje.cual +=1
                if personaje.rect.x >= 680:
                   scroll = True
                   personaje.cambio_x = 0
                if personaje.rect.x < 680:    
                   scroll = False
                   personaje.AvanzarDerecha()

          if tecla[pygame.K_LEFT]:
             personaje.izquierda = True
             FondoDerecha = False
             if CantidadVidas == 0 or FinMeta == True:
                scroll = False
             else:
                if pygame.time.get_ticks()-personaje.tiempo > personaje.cuanto:
                   personaje.tiempo = pygame.time.get_ticks()
                   personaje.cual +=1
                if personaje.rect.x <= 680:
                   scroll = True
                   personaje.cambio_x = 0
                if personaje.rect.x > 680:    
                   scroll = False
                   personaje.AvanzarIzquierda()

          if tecla[pygame.K_UP]:
             sounds.Salto.play()
             personaje.Saltar()
             personaje.cual = 1


          if tecla[pygame.K_DOWN]:
             scroll = False
             personaje.Agacharse()
             personaje.cual = 0
#------------------------------------------------------------------------------------------------------------------------------------------------
          if tecla[pygame.K_ESCAPE]:
             if FinMeta == True or FinGameOver == True:
                Pausa = False
             else:
                Pausa = True
                OpcionMenuPausa = 1
                pygame.mixer.music.pause()
                sounds.Pausa.play(-1)
                while Pausa:
                   reloj.tick(60) 
                   tecla = pygame.key.get_pressed()
                   for event in pygame.event.get():
                      if event.type == pygame.QUIT:
                         pygame.quit()
                      if tecla[pygame.K_UP] and OpcionMenuPausa > 1 and MenuPausaY > DimensionMenuPausa[1]:
                         OpcionMenuPausa -= 1
                         MenuPausaY = MenuPausaY-40
                      if tecla[pygame.K_DOWN] and OpcionMenuPausa < 3 and MenuPausaY > DimensionMenuPausa[0]:
                         OpcionMenuPausa += 1
                         MenuPausaY = MenuPausaY+40
                      if tecla[K_RETURN]:
	                 if OpcionMenuPausa == 1:
	                    print "REANUDAR JUEGO"
                            sounds.Pausa.stop()
                            sounds.EnterMenu.play()
                            Pausa = False
                            pygame.mixer.music.unpause()
	                 if OpcionMenuPausa == 2:
                            print "VOLVER AL MENU PRINCIPAL"
                            sounds.Pausa.stop()
                            sounds.EnterMenu.play()
	                    salir = True
                            Pausa = False
                            pygame.mixer.music.load('Musicafondo.mp3')
                            pygame.mixer.music.play(-1)
                            Menu(opcion)
	                 if OpcionMenuPausa == 3:
                            sounds.EnterMenu.play()
                            sys.exit()
                   MenuPausa(OpcionMenuPausa)
                   pygame.display.update()
#------------------------------------------------------------------------------------------------------------------------------------------------                   
       if event.type == pygame.KEYUP:
          personaje.cual = 3

          if tecla[pygame.K_SPACE]:
             personaje.cual = 2

          if tecla[pygame.K_RIGHT]:
             personaje.Detenerse()
             scroll = False

          if tecla[pygame.K_LEFT]:
             personaje.Detenerse()
             scroll = False
#------------------------------------------------------------------------------------------------------------------------------------------------
       Puntos = FuenteEstadisticas.render("Puntaje = " + str(Puntaje), True, blanco)

       ColisionBalasYellowGrunt = pygame.sprite.groupcollide(DisparosGrupo, personaje.posicionyellowgrunt.ListaYellowGrunt, True, True)
       for yellowgrunt in ColisionBalasYellowGrunt:
          print "+100 Puntos"
          sounds.Salto.stop()
          sounds.Destruido.play()
          yellowgrunt.kill()
          Puntaje += 100
#------------------------------------------------------------------------------------------------------------------------------------------------
       ColisionBalasRedGrunt = pygame.sprite.groupcollide(DisparosGrupo, personaje.posicionredgrunt.ListaRedGrunt, True, True)
       for redgrunt in ColisionBalasRedGrunt:
          print "+100 Puntos"
          sounds.Salto.stop()
          sounds.Destruido.play()
          redgrunt.kill()
          Puntaje += 100
#------------------------------------------------------------------------------------------------------------------------------------------------
       ColisionBalasElite = pygame.sprite.groupcollide(DisparosGrupo, personaje.posicionelite.ListaElite, True, True)
       for elite in ColisionBalasElite:
          print "+300 Puntos"
          sounds.Salto.stop()
          sounds.Destruido.play()
          elite.kill()
          Puntaje += 300
#------------------------------------------------------------------------------------------------------------------------------------------------
       ColisionBalasPlataforma = pygame.sprite.groupcollide(DisparosGrupo, personaje.nivel.ListaPlataformas, True, False)
       for plataforma in ColisionBalasPlataforma:
          sounds.Salto.stop()
#------------------------------------------------------------------------------------------------------------------------------------------------
       Vidas = FuenteEstadisticas.render("Vidas = " + str(CantidadVidas), True, blanco)

       ColisionModificableVidas = pygame.sprite.spritecollide(personaje, personaje.posicionvida.ListaVidas, False)
       for vida in ColisionModificableVidas:
          print "+1 Vida"
          sounds.Salto.stop()
          sounds.MasVida.play()
          vida.kill()
          CantidadVidas += 1
#------------------------------------------------------------------------------------------------------------------------------------------------
       ColisionPersonajeYellowGrunt = pygame.sprite.spritecollide(personaje, personaje.posicionyellowgrunt.ListaYellowGrunt, False)
       for yellowgrunt in ColisionPersonajeYellowGrunt:
          print "-1 Vida"
          sounds.Salto.stop()
          sounds.death.play()
          if CantidadVidas == 0:
             CantidadVidas = 0
             print "GAME OVER"
             FinGameOver = True
             personaje.kill()
             EliminarDisparo = True
             PausaTiempo = True
             sounds.GameOver.play(-1)
          else:
             CantidadVidas -= 1
             yellowgrunt.kill()
#------------------------------------------------------------------------------------------------------------------------------------------------
       ColisionPersonajeRedGrunt = pygame.sprite.spritecollide(personaje, personaje.posicionredgrunt.ListaRedGrunt, False)
       for redgrunt in ColisionPersonajeRedGrunt:
          print "-1 Vida"
          sounds.Salto.stop()
          sounds.death.play()
          if CantidadVidas == 0:
             CantidadVidas = 0
             print "GAME OVER"
             (x, y) = redgrunt.rect.center
             ListaSpritesActivos.add(Explocion(x, y))
             yellowgrunt.kill()
             FinGameOver = True
             redgrunt.kill()
             personaje.kill()
             EliminarDisparo = True
             PausaTiempo = True
             sounds.GameOver.play(-1)
          else:
             (x, y) = redgrunt.rect.center
             ListaSpritesActivos.add(Explocion(x, y))
             yellowgrunt.kill()
             CantidadVidas -= 1
             redgrunt.kill()
#------------------------------------------------------------------------------------------------------------------------------------------------
       ColisionPersonajeElite = pygame.sprite.spritecollide(personaje, personaje.posicionelite.ListaElite, False)
       for elite in ColisionPersonajeElite:
          print "-1 Vida"
          sounds.Salto.stop()
          sounds.death.play()
          if CantidadVidas -2 <= 0:
             CantidadVidas = 0
             print "GAME OVER"
             FinGameOver = True
             elite.kill()
             personaje.kill()
             EliminarDisparo = True
             PausaTiempo = True
             sounds.GameOver.play(-1)
          else:
             CantidadVidas -= 2
             elite.kill()
#------------------------------------------------------------------------------------------------------------------------------------------------
       Balas = FuenteEstadisticas.render("Balas = " + str(CantidadBalas), True, blanco)
       ColisionModificableBalas = pygame.sprite.spritecollide(personaje, personaje.posicionbala.ListaBalas, False)
       for bala in ColisionModificableBalas:
          print "+6 Balas"
          sounds.Salto.stop()
          sounds.MasBala.play()
          bala.kill()
          CantidadBalas += 6
#------------------------------------------------------------------------------------------------------------------------------------------------
       ColisionMeta = pygame.sprite.spritecollide(personaje, personaje.posicionmeta.ListaMeta, False)
       for meta in ColisionMeta:
          print "META, FIN DE NIVEL"
          FinMeta = True
          personaje.kill()
          EliminarDisparo = True
          PausaTiempo = True
          sounds.Meta.play()
#------------------------------------------------------------------------------------------------------------------------------------------------
       Tiempo = FuenteEstadisticas.render("Tiempo = ", True, blanco)

       if CambioNivel2 == True:
          IniciarNivel2()
          pygame.display.flip()
       else:
          FondoAnimadoGrupo.update()
          FondoAnimadoGrupo.draw(pantalla)
          DibujoPlataformas.update()
          DibujoPlataformas.draw(pantalla)
          DibujoYellowGrunt.update()
          DibujoYellowGrunt.draw(pantalla)
          DibujoRedGrunt.update()
          DibujoRedGrunt.draw(pantalla)
          DibujoElite.update()
          DibujoElite.draw(pantalla)
          DibujoVidas.update()
          DibujoVidas.draw(pantalla)
          DibujoBalas.update()
          DibujoBalas.draw(pantalla)
          DibujoMeta.update()
          DibujoMeta.draw(pantalla)

       if personaje.rect.right > ANCHO:
          personaje.rect.right = ANCHO
       if personaje.rect.left < 0:
          personaje.rect.left = 0

       ListaSpritesActivos.update()
       ListaSpritesActivos.draw(pantalla)
       DisparosGrupo.update()
       DisparosGrupo.draw(pantalla)
       DisparosGrupo2.update()
       DisparosGrupo2.draw(pantalla)

       pantalla.blit(Seleccion,(4,4))
       pantalla.blit(IconoVidas,(300,4))
       pantalla.blit(IconoBalas,(530,4))

       pantalla.blit(Puntos,(59,8))
       pantalla.blit(Vidas,(355,8))
       pantalla.blit(Balas,(595,8))
       pantalla.blit(Tiempo,(1130,8))

       if FinGameOver == True or CantidadVidas == 0:
          personaje.kill()
          pygame.mixer.music.stop()
          sounds.GameOver.play(-1)
          pantalla.blit(FondoGameOver,(320,20))
          pantalla.blit(Elite,(800,50))
          pantalla.blit(Halodied,(0,1))
	  Halo = pygame.image.load('Halo.png').convert_alpha()
	  pantalla.blit(Halo,(380,600))
          MovimientoGameOver()
          pantalla.blit(TextoGameOver,(pos6-20,380))
          MovimientoPresioneEspacioGameOver()
          pantalla.blit(TextoPresioneEspacioGameOver,(200,pos15+30))
          if tecla[pygame.K_RETURN]:
             sounds.GameOver.stop()
             pygame.mixer.music.load('Musicafondo.mp3')
             pygame.mixer.music.play(-1)
             salir = True
             python = sys.executable
             os.execl(python, python, * sys.argv)

       if FinMeta == True:
          pygame.mixer.music.stop()
          pantalla.blit(Halo3MC,(500,-30))
          pantalla.blit(MensajeHalo,(380,630))
          MovimientoMision1Completa()
          pantalla.blit(TextoMision1Completa,(pos13,340))
          MovimientoPresioneEspacioMeta()
          pantalla.blit(TextoPresioneEspacioMeta,(450,pos14))
          if tecla[pygame.K_RETURN]:
             sounds.Meta.stop()
             pygame.mixer.music.load('Musicafondo.mp3')
             pygame.mixer.music.play(-1)
             EliminarDisparo = False
             CambioNivel2 = True
             Puntaje += 1000
             CantidadVidas += 5
             CantidadBalas += 10
             personaje.rect.y = BASE_PERSONAJE + 100
             FinMeta = False

       if disparoenemigo == True:
          DisparosGrupo.add(DisparoDerechaEnemy(personaje.rect.right-10, personaje.rect.y+40))

       TiempoJuego()
       cadena=ConcatenacionTiempo(deceMin,unidMin,deceSeg,unidSeg,centSeg)
       textoTiempo.render(pantalla, cadena, blanco, (1235, 8))
       pygame.display.update()    
#------------------------------------------------------------------------------------------------------------------------------------------------
#fin nivel 1--init nivel 2
#------------------------------------------------------------------------------------------------------------------------------------------------
def IniciarNivel2():

    #IMAGEN DE FONDO NIVEL 2
    FondoAnimadoNivel2 = FondoAnimado2(0,0)
    FondoAnimadoGrupo2 = pygame.sprite.RenderUpdates(FondoAnimadoNivel2)
    #CREACION DE PLATAFORMAS NIVEL 2
    GrupoPlataformas2 = []
    GrupoPlataformas2.append(PlataformasNivel2())
    DibujoPlataformas2 = GrupoPlataformas2[0]
    personaje2.nivel2 = DibujoPlataformas2
    #CREACION DE PLATAFORMAS VACIAS
    GrupoPlataformasVacias = []
    GrupoPlataformasVacias.append(LlamasNivel2())
    DibujoPlataformasLlamas = GrupoPlataformasVacias[0]
    personaje2.Llamas2 = DibujoPlataformasLlamas
    #CREACION DE GRUNT AMARRILLO
    GrupoYellowGrunt2 = []
    GrupoYellowGrunt2.append(YellowGruntNivel2())
    DibujoYellowGrunt2 = GrupoYellowGrunt2[0]
    personaje2.posicionyellowgrunt2 = DibujoYellowGrunt2
    #CREACION DE GRUNT ROJO
    GrupoRedGrunt2 = []
    GrupoRedGrunt2.append(RedGruntNivel2())
    DibujoRedGrunt2 = GrupoRedGrunt2[0]
    personaje2.posicionredgrunt2 = DibujoRedGrunt2
    #CREACION DE ELITE
    GrupoElite2 = []
    GrupoElite2.append(EliteNivel2())
    DibujoElite2 = GrupoElite2[0]
    personaje2.posicionelite2 = DibujoElite2
    #CREACION DE JACKAL MAYOR
    GrupoJackalMayor = []
    GrupoJackalMayor.append(JackalMayorNivel1())
    DibujoJackalMayor = GrupoJackalMayor[0]
    personaje2.posicionjackal = DibujoJackalMayor
    #CREACION DE HUNTER
    GrupoHunter = []
    GrupoHunter.append(HunterNivel1())
    DibujoHunter = GrupoHunter[0]
    personaje2.posicionhunter = DibujoHunter
    #CREACION DE BRUTE
    GrupoBrute = []
    GrupoBrute.append(BruteNivel1())
    DibujoBrute = GrupoBrute[0]
    personaje2.posicionbrute = DibujoBrute
    #CREACION DE MODIFICADOR VIDAS
    GrupoVidas2 = []
    GrupoVidas2.append(VidasNivel2())
    DibujoVidas2 = GrupoVidas2[0]
    personaje2.posicionvida2 = DibujoVidas2
    #CREACION DE MODIFICADOR BALAS
    GrupoBalas = []
    GrupoBalas.append(BalasNivel2())
    DibujoBalas = GrupoBalas[0]
    personaje2.posicionbala = DibujoBalas
    #CREACION DE META
    GrupoMeta = []
    GrupoMeta.append(MetaNivel2())
    DibujoMeta = GrupoMeta[0]
    personaje2.posicionmeta = DibujoMeta
    #ICONOS DE OBJETOS
    IconoVidas = pygame.image.load('botiquin2.png').convert_alpha()
    IconoBalas = pygame.image.load('Halogun.png').convert_alpha()
    #PERSONAJE
    PersonajeGrupo = pygame.sprite.RenderUpdates(personaje2)
    personaje2.rect.x = 100
    personaje2.rect.y = 50
    ListaSpritesActivos = pygame.sprite.Group()
    ListaSpritesActivos.add(personaje2)
    #DISPAROS
    DisparosGrupo = pygame.sprite.RenderUpdates()
    DisparosGrupo2 = pygame.sprite.RenderUpdates()
#------------------------------------------------------------------------------------------------------------------------------------------------
    pygame.event.clear
    os.system('clear')
    salir = False
    FinGameOver = False
    FinMeta = False
    pygame.mixer.music.stop()
    pygame.mixer.music.load('Fondohalo.mp3')
    pygame.mixer.music.play(-1)

    FondoGameOver = pygame.image.load('FondoMenuPausa.png').convert_alpha() 
    Elite = pygame.image.load('Elite.png').convert_alpha()
    Halodied = pygame.image.load('halodied.png').convert_alpha()
    FondoMensajeMeta = pygame.image.load('FondoMenuPausa.png').convert_alpha() 
    Halo3MC = pygame.image.load('Halo3MC.png').convert_alpha() 
    MensajeHalo = pygame.image.load('Halo.png').convert_alpha() 

    TextoGameOver = FuenteGameOver.render("GAME OVER", 1, (azul))
    TextoMision1Completa = FuenteMisionCompleta.render("HAS COMPLETADO LA VERSION DEMO..", 1, (blanco))
    TextoPresioneEspacioMeta = FuentePresioneEspacio.render("PRESIONE ENTER PARA CONTINUAR", 1, (amarillo))
    TextoPresioneEspacioGameOver = FuentePresioneEspacio.render("PRESIONE ENTER PARA CONTINUAR", 1, (azul))

    Mas100Puntos = FuentePuntaje.render("+100", 1, (negro))

    global event, movimiento2, FondoDerecha2, EliminarDisparo, MenuPausaY, DimensionMenuPausa, Puntaje
    global centSeg, unidSeg, deceSeg, unidMin, deceMin, PausaTiempo, CambioNivel2, CantidadVidas, CantidadBalas
    while salir != True: 
       reloj.tick(60) 
       tecla = pygame.key.get_pressed()
       for event in pygame.event.get():   
           if event.type == pygame.QUIT:
              salir = True
           if tecla[pygame.K_s]:
              sys.exit()
           if tecla[pygame.K_SPACE]:
                print "Disparar"
                personaje2.cual = 2
                movimiento2 = False
                if CantidadBalas == 0 or CantidadVidas == 0 or FinMeta == True:
                   CantidadBalas = CantidadBalas
                else:
                   sounds.Halo_headgun.play()
                   CantidadBalas -= 1
                   if personaje2.izquierda == True:
                      DisparosGrupo.add(DisparoIzquierda(personaje2.rect.left-10, personaje2.rect.y+40))
                   if personaje2.izquierda == False:
                      DisparosGrupo.add(DisparoDerecha(personaje2.rect.right-10, personaje2.rect.y+40))
#------------------------------------------------------------------------------------------------------------------------------------------------   
       if event.type == pygame.KEYDOWN:

          if tecla[pygame.K_RIGHT]:
             personaje2.izquierda = False
             FondoDerecha2 = True
             if CantidadVidas == 0 or FinMeta == True:
                movimiento2 = False
             else:
                if pygame.time.get_ticks()-personaje2.tiempo > personaje2.cuanto:
                   personaje2.tiempo = pygame.time.get_ticks()
                   personaje2.cual +=1
                if personaje2.rect.x >= 680:
                   movimiento2 = True
                   personaje2.cambio_x = 0
                if personaje2.rect.x < 680:    
                   movimiento2 = False
                   personaje2.AvanzarDerecha()

          if tecla[pygame.K_LEFT]:
             personaje2.izquierda = True
             FondoDerecha2 = False
             if CantidadVidas == 0 or FinMeta == True:
                movimiento2 = False
             else:
                if pygame.time.get_ticks()-personaje2.tiempo > personaje2.cuanto:
                   personaje2.tiempo = pygame.time.get_ticks()
                   personaje2.cual +=1
                if personaje2.rect.x <= 680:
                   movimiento2 = True
                   personaje2.cambio_x = 0
                if personaje2.rect.x > 680:    
                   movimiento2 = False
                   personaje2.AvanzarIzquierda()
  
          if tecla[pygame.K_UP]:
             sounds.Salto.play()
             personaje2.Saltar()
             personaje2.cual = 1

          if tecla[pygame.K_DOWN]:
             personaje2.Agacharse()
             personaje2.cual = 0
#------------------------------------------------------------------------------------------------------------------------------------------------
          if tecla[pygame.K_ESCAPE]:
             if FinMeta == True or FinGameOver == True:
                Pausa = False
             else:
                Pausa = True
                OpcionMenuPausa = 1
                pygame.mixer.music.pause()
                sounds.Pausa.play(-1)
                while Pausa:
                   reloj.tick(60) 
                   tecla = pygame.key.get_pressed()
                   for event in pygame.event.get():
                      if event.type == pygame.QUIT:
                         pygame.quit()
                      if tecla[pygame.K_UP] and OpcionMenuPausa > 1 and MenuPausaY > DimensionMenuPausa[1]:
                         OpcionMenuPausa -= 1
                         MenuPausaY = MenuPausaY-40
                      if tecla[pygame.K_DOWN] and OpcionMenuPausa < 3 and MenuPausaY > DimensionMenuPausa[0]:
                         OpcionMenuPausa += 1
                         MenuPausaY = MenuPausaY+40
                      if tecla[K_RETURN]:
	                 if OpcionMenuPausa == 1:
	                    print "REANUDAR JUEGO"
                            sounds.Pausa.stop()
                            sounds.EnterMenu.play()
                            Pausa = False
                            pygame.mixer.music.unpause()
	                 if OpcionMenuPausa == 2:
                            print "VOLVER AL MENU PRINCIPAL"
                            sounds.Pausa.stop()
                            sounds.EnterMenu.play()
                            Pausa = False
	                    salir = True
                            python = sys.executable
                            os.execl(python, python, * sys.argv)
                            pygame.mixer.music.load('Musicafondo.mp3')
                            pygame.mixer.music.play(-1)
                            Menu(opcion)
	                 if OpcionMenuPausa == 3:
                            sounds.EnterMenu.play()
                            sys.exit()
                   MenuPausa(OpcionMenuPausa)
                   pygame.display.update()
#------------------------------------------------------------------------------------------------------------------------------------------------                   
       if event.type == pygame.KEYUP:
          personaje2.cual = 3

          if tecla[pygame.K_SPACE]:
             personaje2.cual = 2

          if tecla[pygame.K_RIGHT]:
             personaje2.Detenerse()
             movimiento2 = False

          if tecla[pygame.K_LEFT]:
             personaje2.Detenerse()
             movimiento2 = False
#------------------------------------------------------------------------------------------------------------------------------------------------
       Puntos = FuenteEstadisticas.render("Puntaje = " + str(Puntaje), True, blanco)

       ColisionBalasYellowGrunt2 = pygame.sprite.groupcollide(DisparosGrupo, personaje2.posicionyellowgrunt2.ListaYellowGrunt2, True, True)
       for yellowgrunt in ColisionBalasYellowGrunt2:
          print "+100 Puntos"
          sounds.Salto.stop()
          sounds.Destruido.play()
          yellowgrunt.kill()
          Puntaje += 100
#------------------------------------------------------------------------------------------------------------------------------------------------
       ColisionBalasRedGrunt2 = pygame.sprite.groupcollide(DisparosGrupo, personaje2.posicionredgrunt2.ListaRedGrunt2, True, True)
       for redgrunt in ColisionBalasRedGrunt2:
          print "+100 Puntos"
          sounds.Salto.stop()
          sounds.Destruido.play()
          redgrunt.kill()
          Puntaje += 100
#------------------------------------------------------------------------------------------------------------------------------------------------
       ColisionBalasElite2 = pygame.sprite.groupcollide(DisparosGrupo, personaje2.posicionelite2.ListaElite2, True, True)
       for elite in ColisionBalasElite2:
          print "+300 Puntos"
          sounds.Salto.stop()
          sounds.Destruido.play()
          elite.kill()
          Puntaje += 300
#------------------------------------------------------------------------------------------------------------------------------------------------
       ColisionBalasJackal = pygame.sprite.groupcollide(DisparosGrupo, personaje2.posicionjackal.ListaJackalMayor, True, True)
       for jackal in ColisionBalasJackal:
          print "+300 Puntos jackal"
          sounds.Salto.stop()
          sounds.Destruido.play()
          jackal.kill()
          Puntaje += 300
#------------------------------------------------------------------------------------------------------------------------------------------------
       ColisionBalasHunter = pygame.sprite.groupcollide(DisparosGrupo, personaje2.posicionhunter.ListaHunter, True, True)
       for hunter in ColisionBalasHunter:
          print "+500 Puntos"
          sounds.Salto.stop()
          sounds.Destruido.play()
          hunter.kill()
          Puntaje += 500
#-----------------------------------------------------------------------------------------------------------------------------------------------------
       ColisionBalasBrute = pygame.sprite.groupcollide(DisparosGrupo, personaje2.posicionbrute.ListaBrute, True, True)
       for brute in ColisionBalasBrute:
          print "+700 Puntos"
          sounds.Salto.stop()
          sounds.Destruido.play()
          brute.kill()
          CantidadBalas += 2
          CantidadVidas += 2
          Puntaje += 700
#------------------------------------------------------------------------------------------------------------------------------------------------
       ColisionBalasPlataforma2 = pygame.sprite.groupcollide(DisparosGrupo, personaje2.nivel2.ListaPlataformas2, True, False)
       for plataforma in ColisionBalasPlataforma2:
          sounds.Salto.stop()
#------------------------------------------------------------------------------------------------------------------------------------------------
       Vidas = FuenteEstadisticas.render("Vidas = " + str(CantidadVidas), True, blanco)

       ColisionModificableVidas = pygame.sprite.spritecollide(personaje2, personaje2.posicionvida2.ListaVidas2, False)
       for vida in ColisionModificableVidas:
          print "+3 Vida"
          sounds.Salto.stop()
          sounds.MasVida.play()
          vida.kill()
          CantidadVidas += 4
#------------------------------------------------------------------------------------------------------------------------------------------------
       ColisionPersonajeYellowGrunt2 = pygame.sprite.spritecollide(personaje2, personaje2.posicionyellowgrunt2.ListaYellowGrunt2, False)
       for yellowgrunt in ColisionPersonajeYellowGrunt2:
          print "-1 Vida"
          sounds.Salto.stop()
          sounds.death.play()
          if CantidadVidas == 0:
             CantidadVidas = 0
             print "GAME OVER"
             FinGameOver = True
             yellowgrunt.kill()
             personaje2.kill()
             EliminarDisparo = True
             PausaTiempo = True
             sounds.GameOver.play(-1)
          else:
             CantidadVidas -= 1
             yellowgrunt.kill()
#------------------------------------------------------------------------------------------------------------------------------------------------
       ColisionPersonajeRedGrunt2 = pygame.sprite.spritecollide(personaje2, personaje2.posicionredgrunt2.ListaRedGrunt2, False)
       for redgrunt in ColisionPersonajeRedGrunt2:
          print "-1 Vida"
          sounds.Salto.stop()
          sounds.death.play()
          if CantidadVidas == 0:
             CantidadVidas = 0
             print "GAME OVER"
             (x, y) = redgrunt.rect.center
             ListaSpritesActivos.add(Explocion(x, y))
             FinGameOver = True
             redgrunt.kill()
             personaje2.kill()
             EliminarDisparo = True
             PausaTiempo = True
             sounds.GameOver.play(-1)
          else:
             (x, y) = redgrunt.rect.center
             ListaSpritesActivos.add(Explocion(x, y))
             CantidadVidas -= 1
             redgrunt.kill()
#------------------------------------------------------------------------------------------------------------------------------------------------
       ColisionPersonajeElite2 = pygame.sprite.spritecollide(personaje2, personaje2.posicionelite2.ListaElite2, False)
       for elite in ColisionPersonajeElite2:
          print "-1 Vida"
          sounds.Salto.stop()
          sounds.death.play()
          if CantidadVidas -2 <= 0:
             CantidadVidas = 0
             print "GAME OVER"
             FinGameOver = True
             elite.kill()
             personaje2.kill()
             EliminarDisparo = True
             PausaTiempo = True
             sounds.GameOver.play(-1)
          else:
             CantidadVidas -= 2
             elite.kill()
#------------------------------------------------------------------------------------------------------------------------------------------------
       ColisionPersonajeHunter = pygame.sprite.spritecollide(personaje2, personaje2.posicionhunter.ListaHunter, False)
       for hunter in ColisionPersonajeHunter:
           print "-3 Vida"
           sounds.Salto.stop()
           sounds.death.play()
           if CantidadVidas-3 <= 0:
              CantidadVidas = 0
              print "GAME OVER"
              FinGameOver = True
              hunter.kill()
              personaje2.kill()
              EliminarDisparo = True
              PausaTiempo = True
              sounds.GameOver.play(-1)
           else:
              CantidadVidas -= 3
              hunter.kill()
#------------------------------------------------------------------------------------------------------------------------------------------------
       ColisionPersonajeJackalMayor = pygame.sprite.spritecollide(personaje2, personaje2.posicionjackal.ListaJackalMayor, False)
       for jackal in ColisionPersonajeJackalMayor:
           print "-1 Vida"
           sounds.Salto.stop()
           sounds.death.play()
           if CantidadVidas == 0:
              CantidadVidas = 0
              print "GAME OVER"
              FinGameOver = True
              jackal.kill()
              personaje2.kill()
              EliminarDisparo = True
              PausaTiempo = True
              sounds.GameOver.play(-1)
           else:
              CantidadVidas -= 1
              jackal.kill()
#--------------------------------------------------------------------------------------------------------------------------------------------------
       ColisionPersonajeBrute = pygame.sprite.spritecollide(personaje2, personaje2.posicionbrute.ListaBrute, False)
       for brute in ColisionPersonajeBrute:
           print "-4 Vida"
           sounds.Salto.stop()
           sounds.death.play()
           if CantidadVidas-4 <= 0:
              CantidadVidas = 0
              print "GAME OVER"
              FinGameOver = True
              brute.kill()
              personaje2.kill()
              EliminarDisparo = True
              PausaTiempo = True
              sounds.GameOver.play(-1)
           else:
              CantidadVidas -= 4
              brute.kill()
#------------------------------------------------------------------------------------------------------------------------------------------------
       Balas = FuenteEstadisticas.render("Balas = " + str(CantidadBalas), True, blanco)
       ColisionModificableBalas = pygame.sprite.spritecollide(personaje2, personaje2.posicionbala.ListaBalas, False)
       for bala in ColisionModificableBalas:
          print "+6 Balas"
          sounds.Salto.stop()
          sounds.MasBala.play()
          bala.kill()
          CantidadBalas += 6
#------------------------------------------------------------------------------------------------------------------------------------------------
       ColisionMeta = pygame.sprite.spritecollide(personaje2, personaje2.posicionmeta.ListaMeta, False)
       for meta in ColisionMeta:
          print "META, FIN DEL JUEGO"
          FinMeta = True
          personaje2.kill()
          EliminarDisparo = True
          PausaTiempo = True
          sounds.Meta.play()
#------------------------------------------------------------------------------------------------------------------------------------------------
       ColisionLlama = pygame.sprite.spritecollide(personaje2, personaje2.Llamas2.ListaLlamas,False)
       for vacio in ColisionLlama:
          print "+3 Vida"
          sounds.Salto.stop()
          sounds.death.play()
	  vacio.kill()
          CantidadVidas -= 1
#------------------------------------------------------------------------------------------------------------------------------------------------
       Tiempo = FuenteEstadisticas.render("Tiempo = ", True, blanco)


       FondoAnimadoGrupo2.update()
       FondoAnimadoGrupo2.draw(pantalla)
       ListaSpritesActivos.add(personaje2)
       DibujoPlataformas2.update()
       DibujoPlataformas2.draw(pantalla)
       DibujoPlataformasLlamas.update()
       DibujoPlataformasLlamas.draw(pantalla)
       DibujoYellowGrunt2.update()
       DibujoYellowGrunt2.draw(pantalla)
       DibujoRedGrunt2.update()
       DibujoRedGrunt2.draw(pantalla)
       DibujoElite2.update()
       DibujoElite2.draw(pantalla)
       DibujoJackalMayor.update()
       DibujoJackalMayor.draw(pantalla)
       DibujoBrute.update()
       DibujoBrute.draw(pantalla)
       DibujoHunter.update()
       DibujoHunter.draw(pantalla)
       DibujoVidas2.update()
       DibujoVidas2.draw(pantalla)
       DibujoBalas.update()
       DibujoBalas.draw(pantalla)
       DibujoMeta.update()
       DibujoMeta.draw(pantalla)

       if personaje2.rect.right > ANCHO:
          personaje2.rect.right = ANCHO
       if personaje2.rect.left < 0:
          personaje2.rect.left = 0

       ListaSpritesActivos.update()
       ListaSpritesActivos.draw(pantalla)
       DisparosGrupo.update()
       DisparosGrupo.draw(pantalla)

       pantalla.blit(Seleccion,(4,4))
       pantalla.blit(IconoVidas,(300,4))
       pantalla.blit(IconoBalas,(530,4))

       pantalla.blit(Puntos,(59,8))
       pantalla.blit(Vidas,(355,8))
       pantalla.blit(Balas,(595,8))
       pantalla.blit(Tiempo,(1130,8))

       if FinGameOver == True or CantidadVidas == 0:
          personaje2.kill()
          pygame.mixer.music.stop()
          sounds.GameOver.play(-1)
          pantalla.blit(FondoGameOver,(320,20))
          pantalla.blit(Elite,(800,50))
          pantalla.blit(Halodied,(0,1))
	  Halo = pygame.image.load('Halo.png').convert_alpha()
	  pantalla.blit(Halo,(380,600))
          MovimientoGameOver()
          pantalla.blit(TextoGameOver,(pos6-20,380))
          MovimientoPresioneEspacioGameOver()
          pantalla.blit(TextoPresioneEspacioGameOver,(200,pos15+30))
          if tecla[pygame.K_RETURN] or tecla[pygame.K_ESCAPE]:
             sounds.GameOver.stop()
             pygame.mixer.music.load('Musicafondo.mp3')
             pygame.mixer.music.play(-1)
#             FinGameOver = False
#             CambioNivel = False
#             salir = True
             python = sys.executable
             os.execl(python, python, * sys.argv)


       if FinMeta == True:
          pygame.mixer.music.stop()
          pantalla.blit(FondoMensajeMeta,(150,250))
          pantalla.blit(Halo3MC,(380,-20))
          MovimientoMision1Completa()
          pantalla.blit(TextoMision1Completa,(200,340))
          MovimientoPresioneEspacioMeta()
          pantalla.blit(TextoPresioneEspacioMeta,(350,500))
          if tecla[pygame.K_RETURN]:
             sounds.Meta.stop()
             pygame.mixer.music.load('Musicafondo.mp3')
             pygame.mixer.music.play(-1)
             sys.exit()
       TiempoJuego()
       cadena=ConcatenacionTiempo(deceMin,unidMin,deceSeg,unidSeg,centSeg)
       textoTiempo.render(pantalla, cadena, blanco, (1235, 8))
       pygame.display.update()    
#------------------------------------------------------------------------------------------------------------------------------------------------
def Instrucciones():
    salir = False
    FondoInstrucciones = pygame.image.load('FondoInstrucciones.jpg').convert()
    Halo = pygame.image.load('Halo.png').convert_alpha()
    fuente2 = pygame.font.Font('Halo3.ttf', 30)
    Avanzar = fuente2.render("Avanzar", 1, (blanco))
    Retroceder = fuente2.render("Retroceder", 1, (blanco))
    Saltar = fuente2.render("Saltar", 1, (blanco))
    Agacharse = fuente2.render("Agacharse", 1, (blanco))
    Disparar = fuente2.render("Disparar", 1, (blanco))
    Pausar = fuente2.render("Pausar", 1, (blanco))
    pantalla.blit(FondoInstrucciones,(0,0))
    pantalla.blit(Avanzar,(630,265))
    pantalla.blit(Retroceder,(50,320))
    pantalla.blit(Saltar,(500,146))
    pantalla.blit(Agacharse,(400,612))
    pantalla.blit(Disparar,(970,340))
    pantalla.blit(Pausar,(940,536))
    pantalla.blit(Halo,(350,10))

    while salir != True:
       tecla = pygame.key.get_pressed()   
       for event in pygame.event.get():
          if event.type == pygame.QUIT:
             salir = True
          if tecla[pygame.K_ESCAPE]:
             print "REGRESAR AL MENU"
             salir = True
       pygame.display.flip()
#------------------------------------------------------------------------------------------------------------------------------------------------
def Creditos():
    salir = False
    FondoCreditos = pygame.image.load('FondoCreditos.jpg').convert()
    Halo = pygame.image.load('Halo.png').convert_alpha()
    LogoUniversidad = pygame.image.load('LogoUniversidad.png').convert_alpha()
    Computador = pygame.image.load('Computador.png').convert_alpha()
    fuente = pygame.font.Font('Halo3.ttf', 70)
    fuente3 = pygame.font.Font('Halo3.ttf', 30)
    Nombre1 = fuente3.render("David Beltran Coy", 1, (azul))
    Nombre2 = fuente3.render("Oscar Miticanoy", 1, (azul))
    while salir != True:
       reloj.tick(60) 
       tecla = pygame.key.get_pressed()   
       for event in pygame.event.get():
          if event.type == pygame.QUIT:
             salir = True
          if tecla[pygame.K_ESCAPE]:
             print "REGRESAR AL MENU"
             salir = True
       pantalla.blit(FondoCreditos,(0,0))
       pantalla.blit(Halo,(350,10))
       MovimientoLogoUniversidad()
       pantalla.blit(LogoUniversidad,(pos8,350))
       MovimientoComputador()
       pantalla.blit(Computador,(pos8,500))
       MovimientoNombre1()
       pantalla.blit(Nombre1,(500,pos11))
       MovimientoNombre2()
       pantalla.blit(Nombre2,(500,pos12))
       pygame.display.flip()
#------------------------------------------------------------------------------------------------------------------------------------------------
# Menu Inicial
def Menu(opcion):
    Fondo = pygame.image.load('Imageninicio.jpg').convert()
    fuente = pygame.font.Font('Halo3.ttf', 80)
    pantalla.blit(Fondo,(0,0))
    if opcion == 1:
       IniciarJuego,opcion1 = TextoMenu("INICIAR  JUEGO",300,240,(azul))
       Instrucciones,opcion2 = TextoMenu("INSTRUCCIONES",300,290,(negro))
       Historia,opcion3=TextoMenu("HISTORIA",300,340,(negro))
       Creditos,opcion4 = TextoMenu("CREDITOS",300,390,(negro))
       Salir,opcion5 = TextoMenu("SALIR",300,440,(negro))
    if opcion == 2:      
       IniciarJuego,opcion1 = TextoMenu("INICIAR  JUEGO",300,240,(negro))
       Instrucciones,opcion2 = TextoMenu("INSTRUCCIONES",300,290,(azul))
       Historia,opcion3=TextoMenu("HISTORIA",300,340,(negro))
       Creditos,opcion4 = TextoMenu("CREDITOS",300,390,(negro))
       Salir,opcion5 = TextoMenu("SALIR",300,440,(negro))
    if opcion == 3:
       IniciarJuego,opcion1 = TextoMenu("INICIAR  JUEGO",300,240,(negro))
       Instrucciones,opcion2 = TextoMenu("INSTRUCCIONES",300,290,(negro))
       Historia,opcion3=TextoMenu("HISTORIA",300,340,(azul))
       Creditos,opcion4 = TextoMenu("CREDITOS",300,390,(negro))
       Salir,opcion5 = TextoMenu("SALIR",300,440,(negro))
    if opcion == 4:
       IniciarJuego,opcion1 = TextoMenu("INICIAR  JUEGO",300,240,(negro))
       Instrucciones,opcion2 = TextoMenu("INSTRUCCIONES",300,290,(negro))
       Historia,opcion3=TextoMenu("HISTORIA",300,340,(negro))
       Creditos,opcion4 = TextoMenu("CREDITOS",300,390,(azul))
       Salir,opcion5 = TextoMenu("SALIR",300,440,(negro))
    if opcion == 5:
       IniciarJuego,opcion1 = TextoMenu("INICIAR  JUEGO",300,240,(negro))
       Instrucciones,opcion2 = TextoMenu("INSTRUCCIONES",300,290,(negro))
       Historia,opcion3=TextoMenu("HISTORIA",300,340,(negro))
       Creditos,opcion4 = TextoMenu("CREDITOS",300,390,(negro))
       Salir,opcion5 = TextoMenu("SALIR",300,440,(azul))
    pantalla.blit(IniciarJuego,opcion1)
    pantalla.blit(Instrucciones,opcion2)
    pantalla.blit(Historia,opcion3)
    pantalla.blit(Creditos,opcion4)
    pantalla.blit(Salir,opcion5)
#------------------------------------------------------------------------------------------------------------------------------------------------
def Historia():
    salir = False
    FondoInstrucciones = pygame.image.load('covenant1.jpg').convert()
    FondoI = pygame.image.load('fon3.jpg').convert()
    FondoII=pygame.image.load('descarga.jpg').convert()
    FondoIII=pygame.image.load('images.jpg').convert()
    pantalla.blit(FondoInstrucciones,(0,0))
    flechaarriba = pygame.image.load('arriba.jpg').convert_alpha()
    flechaabajo = pygame.image.load('abajo.jpg').convert_alpha()
    flechaizquierda = pygame.image.load('derecha.jpg').convert_alpha()
    flechaderecha = pygame.image.load('izquierda.jpg').convert_alpha()
    esc= pygame.image.load('esc.jpg').convert_alpha()
    IconoVidas = pygame.image.load('botiquin.png').convert_alpha()
    IconoBalas = pygame.image.load('Halogun.png').convert_alpha()
    fuente3 = pygame.font.Font('Halo3.ttf', 40)
    w1 = fuente3.render("Bienvenido al mundo de Halo", 1, (negro))
    w2 = fuente3.render("aqui conoceras la historia de este juego", 1, (negro))
    pantalla.blit(w1,(160,200))
    pantalla.blit(w2,(160,250))
    pantalla.blit(flechaarriba,(1100,550))
    while salir != True:
       tecla = pygame.key.get_pressed()   
       for event in pygame.event.get():
          if tecla[pygame.K_UP]:
                  pantalla.blit(FondoI,(0,0))
                  fuente3 = pygame.font.Font('Halo3.ttf', 25)
                  intro1 = fuente3.render("El Jefe Maestro nacio el 7 de marzo de 2511 y paso la primera parte de su  ", 1, (blanco))
                  intro2 = fuente3.render("niÃ±ez en el planeta humano Eridanus 2,colonia donde vivio con su familia.",1,(blanco))
                  intro3 = fuente3.render("John era alto para su edad en ese entonces, media aproximadamente un pie mas " , 1, (blanco))
                  intro4 = fuente3.render("que sus companeros de la escuela, lo que lo hacÃ­a una muestra genetica " , 1, (blanco))
                  intro5 = fuente3.render(" perfecta para el proyecto SPARTAN-II Lo describen en la edad de seis  " , 1, (blanco))
                  intro6 = fuente3.render("aÃ±os como un tÃ­pico muchacho, de pielcaucasica, con pelo marron, pecas y " , 1, (blanco))
                  intro7 = fuente3.render(" un espacio entre sus dos dientes delanteros." , 1, (blanco))
                  pantalla.blit(intro1,(160,200))
                  pantalla.blit(intro2,(160,230))
                  pantalla.blit(intro3,(160,260))
                  pantalla.blit(intro4,(160,290))
                  pantalla.blit(intro5,(160,320))
                  pantalla.blit(intro6,(160,350))
                  pantalla.blit(intro7,(160,380))
                  pantalla.blit(flechaabajo,(1100,550))

          if tecla[pygame.K_DOWN]:
                  pantalla.blit(FondoII,(0,0))
                  fuente3 = pygame.font.Font('Halo3.ttf', 25)
                  p1 = fuente3.render("En 2517, John y otros 74 ninos de su edad, fueron secuestrados  ", 1, (blanco))
                  p2 = fuente3.render("secretamente de sus hogares y sustituidos por clones flash " ,1,(blanco))
                  p3 = fuente3.render("(clones que estaban programados para morir en un tiempo " , 1,(blanco))
                  p4 = fuente3.render("determinado). Esta forma especifica de copia fue empleada  " , 1, (blanco))
                  p5 = fuente3.render("para asegurarse de que ninguna de las familias se enteraran  " , 1, (blanco))
                  p6 = fuente3.render("que sus hijos habian sido secuestrados. Sin embargo, los clones " , 1, (blanco))
		  p7=  fuente3.render("resultaron inestables y todos perecieron poco despues de lo ",1,(blanco))
		  p8= fuente3.render(" que fue llamado como la falla metabolica en cascada ",1,(blanco))
                  pantalla.blit(p1,(160,200))
                  pantalla.blit(p2,(160,230))
                  pantalla.blit(p3,(160,260))
                  pantalla.blit(p4,(160,290))
                  pantalla.blit(p5,(160,320))
                  pantalla.blit(p6,(160,350))
	          pantalla.blit(p7,(160,380))
                  pantalla.blit(p8,(160,410))
                  pantalla.blit(flechaizquierda,(1100,550))


          if tecla[pygame.K_LEFT]:
                  pantalla.blit(FondoInstrucciones,(0,0))
                  fuente3 = pygame.font.Font('Halo3.ttf', 25)
                  p1 = fuente3.render(" lo que hace parecer que el deceso fue por causas naturales.  ", 1, (blanco))
                  p2 = fuente3.render("La doctora Catherine Halsey,jefa del proyecto SPARTAN-II, ",1,(blanco))
                  p3 = fuente3.render("comento mÃ¡s adelante que este efecto secundario era " , 1, (blanco))
                  p4 = fuente3.render("desafortunado, pero la fecha lÃ­mite del proyecto no dejaba " , 1, (blanco))
                  p5 = fuente3.render("otra alternativa. Los niÃ±os originales fueron llevados al  " , 1, (blanco))
                  p6 = fuente3.render("planeta Reach, una de las jefaturas del UNSC, para entrenarlos , " , 1, (blanco))
                  p7 = fuente3.render("y convertirlos en supersoldados clase SPARTAN-II.En Reach, los ",1,(blanco))
                  p8 = fuente3.render("ninos secuestrados comenzaron el intensivo entrenamiento fisico",1,(blanco))
                  pantalla.blit(p1,(160,200))
                  pantalla.blit(p2,(160,230))
                  pantalla.blit(p3,(160,260))
                  pantalla.blit(p4,(160,290))
                  pantalla.blit(p5,(160,320))
                  pantalla.blit(p6,(160,350))
                  pantalla.blit(p7,(160,380))
                  pantalla.blit(p8,(160,410))
                  pantalla.blit(flechaderecha,(1100,550))

          if tecla[pygame.K_RIGHT]:
                  pantalla.blit(FondoIII,(0,0))
                  fuente3 = pygame.font.Font('Halo3.ttf', 25)
                  p1 = fuente3.render("mental y psicologico como parte del programa Spartan por parte de  ", 1, (blanco))
                  p2 = fuente3.render("Chief Petty Officer Mendez, asignandoles nuevos nÃºmeros de  ",1,(blanco))
                  p3 = fuente3.render("identificacion en vez de los nombres pasados." , 1, (blanco))
                  p4 = fuente3.render("John Fletcher es ahora John-117." , 1, (blanco))
                  p5 = fuente3.render("Este personaje es el encargado de salvar a la Humanidad de la " , 1,(blanco))
                  p6 = fuente3.render("invasion de los covenant que se quieren apoderarse de la tierra" , 1,(blanco))
                  pantalla.blit(p1,(160,200))
                  pantalla.blit(p2,(160,230))
                  pantalla.blit(p3,(160,260))
                  pantalla.blit(p4,(160,290))
                  pantalla.blit(p5,(160,320))
                  pantalla.blit(p6,(160,350))
                  pantalla.blit(esc,(1100,550))



          if tecla[pygame.K_ESCAPE]:
             print "REGRESAR AL MENU"
             salir = True
       pygame.display.flip()
#------------------------------------------------------------------------------------------------------------------------------------------------
def MenuPausa(OpcionMenuPausa):
    FondoMenuPausa = pygame.image.load('FondoMenuPausa.png').convert_alpha() 
    halopausa1 = pygame.image.load('halopausa1.png').convert_alpha() 
    halopausa2 = pygame.image.load('halopausa2.png').convert_alpha() 
    pantalla.blit(FondoMenuPausa,(330,150))
    pantalla.blit(halopausa1,(20,100))
    pantalla.blit(halopausa2,(750,100))
    if OpcionMenuPausa == 1:
       ReanudarJuego,OpcionMenuPausa1 = TextoMenuPausa("REANUDAR JUEGO",710,300,(azul))
       VolverMenuPrincipal,OpcionMenuPausa2 = TextoMenuPausa("MENU PRINCIPAL",710,370,(negro))
       SalirEscritorio,OpcionMenuPausa3 = TextoMenuPausa("SALIR AL ESCRITORIO",710,440,(negro))
    if OpcionMenuPausa == 2:
       ReanudarJuego,OpcionMenuPausa1 = TextoMenuPausa("REANUDAR JUEGO",710,300,(negro))
       VolverMenuPrincipal,OpcionMenuPausa2 = TextoMenuPausa("MENU PRINCIPAL",710,370,(azul))
       SalirEscritorio,OpcionMenuPausa3 = TextoMenuPausa("SALIR AL ESCRITORIO", 710, 440,(negro))
    if OpcionMenuPausa == 3:
       ReanudarJuego,OpcionMenuPausa1 = TextoMenuPausa("REANUDAR JUEGO",710,300,(negro))
       VolverMenuPrincipal,OpcionMenuPausa2 = TextoMenuPausa("MENU PRINCIPAL",710,370,(negro))
       SalirEscritorio,OpcionMenuPausa3 = TextoMenuPausa("SALIR AL ESCRITORIO", 710, 440,(azul))
    pantalla.blit(ReanudarJuego,OpcionMenuPausa1)
    pantalla.blit(VolverMenuPrincipal,OpcionMenuPausa2)
    pantalla.blit(SalirEscritorio,OpcionMenuPausa3)
#------------------------------------------------------------------------------------------------------------------------------------------------
opcion = 1
while salir != True:
    reloj.tick(60) 
    tecla = pygame.key.get_pressed()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            salir = True
        if tecla[pygame.K_s]:
	    sys.exit()
        if tecla[pygame.K_UP] and opcion > 1 and MenuY > DimensionMenu[1]:
            opcion -= 1
            MenuY = MenuY-40
            Seleccion
        if tecla[pygame.K_DOWN] and opcion < 5 and MenuY > DimensionMenu[0]:
            opcion += 1
            MenuY = MenuY+40
            Seleccion
	if tecla[K_RETURN]:
	    if opcion == 1:
	       print "ACCEDER AL JUEGO"
               sounds.EnterMenu.play()
               IniciarJuego()
               ReiniciarTiempo = True
	    if opcion == 2:
               print "ACCEDER A LAS INSTRUCCIONES"
               sounds.EnterMenu.play()
               Instrucciones()
	    if opcion==3:
	       print "ACCEDER A HISTORIA"
	       sounds.EnterMenu.play()
	       Historia()
	    if opcion == 4:
               print "ACCEDER A LOS CREDITOS"
               sounds.EnterMenu.play()
               Creditos()
	    if opcion == 5:
	       sys.exit()
    Menu(opcion)
    pygame.display.flip()
pygame.quit()

