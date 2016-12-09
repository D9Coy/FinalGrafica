import sys
from pygame.locals import *
from librerias import *

class Juego:
    
  # valores constantes
  #Dimenciones de la pantalla

  def __init__(self):      
    self.Ancho = 800
    self.Alto = 600
    self.NEGRO=(0,0,0)

    #grupos de sprites
    self.lista_todos = pygame.sprite.Group()
    self.lista_plataformas = pygame.sprite.Group()
    self.lista_enemigos = pygame.sprite.Group()
    self.lista_temporal = pygame.sprite.Group()

    self.terminar=False
    self.iniciar_juego=False
    self.pausa=False


  def Cargar(self):
  # #cramos la pantalla
    pygame.init()
    self.pos_pantalla = 0
    self.pantalla = pygame.display.set_mode((self.Ancho, self.Alto))
    self.fondo=pygame.image.load("mapa1.png")
    self.pantalla.blit(self.fondo, (0,0))


    #creamos al jugador
    self.jugador = Jugador()
    self.lista_todos.add(self.jugador)
    self.jugador.plataformas = self.lista_plataformas
    self.jugador.todos = self.lista_todos
    self.jugador.enemigos = self.lista_enemigos

    #creamos los enemigos
    archivo = open("enemigo_1/posicion.txt", "r")
    linea = archivo.readline()
    while linea != "":
      a = int(linea)
      linea = archivo.readline()
      b = int(linea)
      linea = archivo.readline()
      enemigo = Enemigo_1(a, b)
      enemigo.jugador = self.jugador
      enemigo.todos = self.lista_todos
      self.lista_todos.add(enemigo)
      self.lista_enemigos.add(enemigo)
    archivo.close()
    archivo = open("enemigo_2/posicion.txt", "r")
    linea = archivo.readline()
    while linea != "":
      a = int(linea)
      linea = archivo.readline()
      b = int(linea)
      linea = archivo.readline()
      enemigo = Enemigo_2(a, b)
      enemigo.jugador = self.jugador
      enemigo.todos = self.lista_todos
      self.lista_todos.add(enemigo)
      self.lista_enemigos.add(enemigo)
    archivo.close()
    archivo = open("enemigo_3/posicion.txt", "r")
    linea = archivo.readline()
    while linea != "":
      a = int(linea)
      linea = archivo.readline()
      b = int(linea)
      linea = archivo.readline()
      enemigo = Enemigo_3(a, b)
      enemigo.jugador = self.jugador
      enemigo.todos = self.lista_todos
      self.lista_todos.add(enemigo)
      self.lista_enemigos.add(enemigo)
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
      self.lista_todos.add(plataforma)
      self.lista_plataformas.add(plataforma)
    archivo.close()


  def Reiniciar(self):
    self.lista_todos = pygame.sprite.Group()
    self.lista_plataformas = pygame.sprite.Group()
    self.lista_enemigos = pygame.sprite.Group()
    self.lista_temporal = pygame.sprite.Group()
    self.Cargar()
    self.Continuar()
    self.Iniciar()

  def Opciones(self):
    print "opciones"

  def Salir(self):
    self.terminar=True
    pygame.quit()


  def Continuar(self):
    self.iniciar_juego=True
    self.pausa=False

  def Creditos(self):
    print "creditos"



  def Iniciar(self):
    self.relog = pygame.time.Clock()
    
    self.sonido = pygame.mixer.Sound("fondo.wav")
    self.sonido.play()
    self.text = pygame.font.Font(None, 30)
    self.opciones_inicio = [
    ("Jugar", self.Continuar), 
    ("Opciones", self.Opciones), 
    ("Creditos", self.Creditos), 
    ("Salir", self.Salir)
    ]

    self.opciones_pausa = [
    ("Continuar", self.Continuar), 
    ("Nuevo Juego", self.Reiniciar),
    ("Opciones", self.Opciones), 
    ("Creditos", self.Creditos), 
    ("Salir", self.Salir)
    ]
    self.menu_inicio=MENU(self.opciones_inicio, [(255,0,0), ((255,255,255))])
    self.menu_pausa=MENU(self.opciones_pausa, [(255,0,0), ((255,255,255))])

    print "entrando al primer while"
    
    while not self.iniciar_juego and not self.terminar :

      self.relog.tick(20)
      pygame.display.flip()
      for event in pygame.event.get():
        if(event.type == pygame.QUIT):
            self.salir()
      
      self.menu_inicio.imprimir(self.pantalla)
      self.menu_inicio.actualizar()
      


    print "entrando al 2 while"
    if(self.iniciar_juego):
      while(not self.terminar):
        self.relog.tick(20)
        pygame.display.flip()
        for event in pygame.event.get():
          #para salir del juego 
          if(event.type == pygame.QUIT):
            self.terminar=True
          #movimiento del personaje

          if self.pausa:
            self.menu_pausa.imprimir(self.pantalla)
            self.menu_pausa.actualizar()
          else:
            if event.type == pygame.KEYDOWN:
                #Apreta escape para ver menu de pausa 
                if(event.key == pygame.K_ESCAPE):
                    self.pausa=True
                if(event.key == pygame.K_RIGHT):
                    self.jugador.direccion = "derecha"
                #movimiento a la izquierda
                if(event.key == pygame.K_LEFT):
                    self.jugador.direccion ="izquierda"
                if(event.key == pygame.K_UP):
                    if(self.jugador.Coliciones_y() == False):
                      self.jugador.salto = 1
                if(event.key == pygame.K_x):
                  if(self.jugador.salto == 0 and self.jugador.Coliciones_y() == False and self.jugador.direccion == None):
                    self.jugador.golpe = 1
                if(event.key == pygame.K_z):
                  if(self.jugador.salto == 0 and self.jugador.Coliciones_y() == False and self.jugador.direccion == None):
                    self.jugador.disparo = 1

            #cuando soltamos la tecla
            if event.type == pygame.KEYUP:
                if(event.key == pygame.K_RIGHT and self.jugador.direccion == "derecha"):
                    self.jugador.Quieto()
                if(event.key == pygame.K_LEFT and self.jugador.direccion == "izquierda"):
                    self.jugador.Quieto()
        
        if not self.pausa:
          if(self.jugador.vida > 0):          
            self.lista_todos.update()
            self.pos_pantalla += self.jugador.Mover_pantalla(self.lista_todos)
            self.pantalla.blit(self.fondo,(self.pos_pantalla,0))
            self.lista_todos.draw(self.pantalla)
            self.jugador.puntaje = str(self.jugador.puntaje)
            self.texto=self.text.render(self.jugador.puntaje, True, self.NEGRO)
            self.jugador.puntaje = int(self.jugador.puntaje)
            self.texto_rect=self.texto.get_rect()
            self.pantalla.blit(self.texto, [700, 10])
            self.pos_vida = 10
            for i in range(self.jugador.vida):
              self.vida=pygame.image.load("jugador/vida.png")
              self.pantalla.blit(self.vida, (self.pos_vida,0))
              self.pos_vida += 35
          else:
            self.texto=text.render("PERDISTE", True, self.NEGRO)
            self.texto_rect=self.texto.get_rect()
            self.texto_x=self.pantalla.get_width()/2 - self.texto_rect.width/2
            self.texto_y=self.pantalla.get_height()/2 - self.texto_rect.height/2
            self.pantalla.blit(self.texto, [self.texto_x, self.texto_y])
        




juego=Juego()
juego.Cargar()
juego.Iniciar()