import pygame
import sys
from pygame.locals import *
from librerias import *

# valores constantes
#Dimenciones de la pantalla
Ancho = 800
Alto = 600
NEGRO=(0,0,0)

#grupos de sprites
lista_todos = pygame.sprite.Group()
lista_plataformas = pygame.sprite.Group()
lista_enemigos = pygame.sprite.Group()
lista_temporal = pygame.sprite.Group()
# #cramos la pantalla
pygame.init()
pos_pantalla = 0
pantalla = pygame.display.set_mode((Ancho, Alto))
fondo=pygame.image.load("mapa1.png")
pantalla.blit(fondo, (0,0))


#creamos al jugador
jugador = Jugador()
lista_todos.add(jugador)
jugador.plataformas = lista_plataformas
jugador.todos = lista_todos
jugador.enemigos = lista_enemigos

#creamos los enemigos
archivo = open("enemigo_1/posicion.txt", "r")
linea = archivo.readline()
while linea != "":
  a = int(linea)
  linea = archivo.readline()
  b = int(linea)
  linea = archivo.readline()
  enemigo = Enemigo_1(a, b)
  enemigo.jugador = jugador
  enemigo.todos = lista_todos
  lista_todos.add(enemigo)
  lista_enemigos.add(enemigo)
archivo.close()
archivo = open("enemigo_2/posicion.txt", "r")
linea = archivo.readline()
while linea != "":
  a = int(linea)
  linea = archivo.readline()
  b = int(linea)
  linea = archivo.readline()
  enemigo = Enemigo_2(a, b)
  enemigo.jugador = jugador
  enemigo.todos = lista_todos
  lista_todos.add(enemigo)
  lista_enemigos.add(enemigo)
archivo.close()
archivo = open("enemigo_3/posicion.txt", "r")
linea = archivo.readline()
while linea != "":
  a = int(linea)
  linea = archivo.readline()
  b = int(linea)
  linea = archivo.readline()
  enemigo = Enemigo_3(a, b)
  enemigo.jugador = jugador
  enemigo.todos = lista_todos
  lista_todos.add(enemigo)
  lista_enemigos.add(enemigo)
archivo.close()

#nivel 1
#crenado las plataformas
archivo = open("dimenciones_nivel1.txt", "r")
linea = archivo.readline()
while linea != "":
  a = int(linea)
  linea = archivo.readline()
  b = int(linea)
  linea = archivo.readline()
  c = int(linea)
  linea = archivo.readline()
  d = int(linea)
  linea = archivo.readline()
  plataforma = Plataforma(a,b,c,d)
  lista_todos.add(plataforma)
  lista_plataformas.add(plataforma)
archivo.close()



relog = pygame.time.Clock()
terminar=False
sonido = pygame.mixer.Sound("fondo.wav")
sonido.play()
text = pygame.font.Font(None, 30)
while(not terminar):
  relog.tick(20)
  for event in pygame.event.get():
    #para salir del juego 
    if(event.type == pygame.QUIT):
      terminar=True
    #movimiento del personaje
    if event.type == pygame.KEYDOWN:
        #movimiento a la derecha 
        if(event.key == pygame.K_RIGHT):
            jugador.direccion = "derecha"
        #movimiento a la izquierda
        if(event.key == pygame.K_LEFT):
            jugador.direccion ="izquierda"
        if(event.key == pygame.K_UP):
            if(jugador.Coliciones_y() == False):
              jugador.salto = 1
        if(event.key == pygame.K_x):
          if(jugador.salto == 0 and jugador.Coliciones_y() == False and jugador.direccion == None):
            jugador.golpe = 1
        if(event.key == pygame.K_z):
          if(jugador.salto == 0 and jugador.Coliciones_y() == False and jugador.direccion == None):
            jugador.disparo = 1

    #cuando soltamos la tecla
    if event.type == pygame.KEYUP:
        if(event.key == pygame.K_RIGHT and jugador.direccion == "derecha"):
            jugador.Quieto()
        if(event.key == pygame.K_LEFT and jugador.direccion == "izquierda"):
            jugador.Quieto()
            
  if(jugador.vida > 0):          
    lista_todos.update()
    pos_pantalla += jugador.Mover_pantalla(lista_todos)
    pantalla.blit(fondo,(pos_pantalla,0))
    lista_todos.draw(pantalla)
    jugador.puntaje = str(jugador.puntaje)
    texto=text.render(jugador.puntaje, True, NEGRO)
    jugador.puntaje = int(jugador.puntaje)
    texto_rect=texto.get_rect()
    pantalla.blit(texto, [700, 10])
    pos_vida = 10
    for i in range(jugador.vida):
      vida=pygame.image.load("jugador/vida.png")
      pantalla.blit(vida, (pos_vida,0))
      pos_vida += 35
  else:
    texto=text.render("PERDISTE", True, NEGRO)
    texto_rect=texto.get_rect()
    texto_x=pantalla.get_width()/2 - texto_rect.width/2
    texto_y=pantalla.get_height()/2 - texto_rect.height/2
    pantalla.blit(texto, [texto_x, texto_y])
  pygame.display.flip()
