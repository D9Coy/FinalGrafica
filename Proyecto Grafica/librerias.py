# -*- coding: utf-8 -*-

import pygame
from pygame.locals import *
import random


class Plataforma(pygame.sprite.Sprite):


    def __init__(self, ancho, alto, pos_x, pos_y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface([ancho, alto], pygame.SRCALPHA, 32)
        self.rect = self.image.get_rect()
        self.rect.x = pos_x
        self.rect.y = pos_y
        self.ancho = ancho
        self.alto = alto

class Bala_enemiga(pygame.sprite.Sprite):
    def __init__(self, pos):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("enemigo_3/bala.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.top = pos.rect.top
        self.rect.right = pos.rect.left + 8
        self.todos = pos.todos
        self.jugador = pos.jugador

    def Colicion(self):
        if(pygame.sprite. collide_rect(self.jugador, self) == True):
            self.jugador.Perder_vida()

class Enemigo_3(pygame.sprite.Sprite):

    def __init__(self, pos_x, pos_y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("enemigo_3/ataque_1.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.tam_x , self.tam_y = self.image.get_size()
        self.rect.x = pos_x
        self.rect.y = pos_y - self.tam_y
        self.movimiento = 1
        self.vulnerable = 0
        self.ataque = 0
        self.jugador = None
        self.todos = None
        self.movimiento = 1
        self.ataque = 0
        self.contador = 0
        self.velocidad = 10
        self.contador_m = 0
        self.movimiento_temp = 0

    def Ataque(self):
        if(self.ataque > 0 and self.ataque < 12):
            self.vulnerable = 0
            temp_x = self.rect.right
            temp_y = self.rect.bottom
            self.ataque = str(self.ataque)
            self.image = pygame.image.load("enemigo_3/ataque_"+ self.ataque +".png").convert_alpha()
            self.rect = self.image.get_rect()
            self.rect.right = temp_x
            self.rect.bottom = temp_y
            self.ataque = int(self.ataque)
            if(self.ataque == 10):
                if(self.contador_m == 0):
                    self.bala = Bala_enemiga(self)
                    self.todos.add(self.bala)
                if(self.contador_m == 20):
                    self.ataque += 1
                    self.contador_m = 0
                    self.todos.remove(self.bala)
                else:
                    self.bala.Colicion()
                    self.contador_m += 1
            else:
                self.ataque += 1
        else:
            self.ataque = 0

    def Descanso(self):
        if(self.ataque == 0):
            if(self.contador < 40):
                self.vulnerable = 1
                temp_x = self.rect.right
                temp_y = self.rect.bottom
                self.image = pygame.image.load("enemigo_3/descanso.png").convert_alpha()
                self.rect = self.image.get_rect()
                self.rect.right = temp_x
                self.rect.bottom = temp_y
                self.contador += 1
            else:
                self.contador = 0
                self.ataque = 1

    def update(self):
        self.Ataque()
        self.Descanso()



class Enemigo_2(pygame.sprite.Sprite):
 
    def __init__(self, pos_x, pos_y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("enemigo_2/quieto_1.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.tam_x , self.tam_y = self.image.get_size()
        self.rect.x = pos_x
        self.rect.y = pos_y - self.tam_y
        self.movimiento = 1
        self.vulnerable = 0
        self.ataque = 0
        self.jugador = None
        self.todos = None
        self.movimiento = 1
        self.ataque = 0
        self.contador = 0
        self.velocidad = 10
        self.contador_m = 0
        self.movimiento_temp = 0

    def Movimiento(self):
        temp_x = self.rect.x
        temp_y = self.rect.bottom
        self.vulnerable = 0
        if(self.movimiento > 0  and self.movimiento < 5):
            self.movimiento = str(self.movimiento)
            self.image = pygame.image.load("enemigo_2/mover_"+ self.movimiento +".png").convert_alpha()
            self.rect = self.image.get_rect()
            self.rect.x = temp_x
            self.rect.bottom = temp_y
            self.movimiento = int(self.movimiento)
            if(self.movimiento == 3):
                if(self.contador_m == 30):
                    self.movimiento += 1
                    self.contador_m = 0
                else:
                    self.contador_m += 1
            else:
                self.movimiento += 1
        else:
            self.movimiento = 0


    

    def Quieto(self):
        if(self.movimiento == 0 and self.ataque == 0):
            if(self.contador < 30):
                self.vulnerable = 1
                temp_x = self.rect.x
                temp_y = self.rect.bottom
                self.image = pygame.image.load("enemigo_2/quieto_1.png").convert_alpha()
                self.rect = self.image.get_rect()
                self.rect.x = temp_x
                self.rect.bottom = temp_y
                self.contador += 1
            else:
                self.contador = 0
                self.ataque = 1

    def Ataque(self):
        if(self.ataque > 0 and self.ataque < 10):
            self.vulnerable = 0
            temp_x = self.rect.right
            temp_y = self.rect.bottom
            self.ataque = str(self.ataque)
            self.image = pygame.image.load("enemigo_2/ataque_"+ self.ataque +".png").convert_alpha()
            self.rect = self.image.get_rect()
            self.rect.right = temp_x
            self.rect.bottom = temp_y
            self.ataque = int(self.ataque)
            self.ataque += 1
            if(pygame.sprite. collide_rect(self.jugador, self) == True):
                self.jugador.Perder_vida()
        if(self.ataque == 10):
            self.ataque = 0
            self.movimiento = 1


    def update(self):
        self.Movimiento()
        self.Quieto()
        self.Ataque()
        

class Enemigo_1(pygame.sprite.Sprite):

    def __init__(self, pos_x, pos_y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("enemigo_1/quieto_1.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.tam_x , self.tam_y = self.image.get_size()
        self.rect.x = pos_x
        self.rect.y = pos_y - self.tam_y - 4
        self.movimiento = 1
        self.vulnerable = 0
        self.ataque = 0
        self.jugador = None
        self.todos = None

    def Movimiento(self):
        if(self.movimiento < 11 and self.movimiento > 0):
            temp_x = self.rect.x
            temp_y = self.rect.bottom
            self.movimiento = str(self.movimiento)
            self.image = pygame.image.load("enemigo_1/quieto_" + self.movimiento + ".png").convert_alpha()
            self.rect = self.image.get_rect()
            self.rect.x = temp_x
            self.rect.bottom = temp_y
            self.movimiento = int(self.movimiento)
            self.movimiento += 1
            self.vulnerable = 1
        else:
            if(self.movimiento < 20 and self.movimiento > 10):
                temp_x = self.rect.x
                temp_y = self.rect.bottom
                self.movimiento += -10
                self.movimiento = str(self.movimiento)
                self.image = pygame.image.load("enemigo_1/ataque_" + self.movimiento + ".png").convert_alpha()
                self.rect = self.image.get_rect()
                self.rect.x = temp_x
                self.rect.bottom = temp_y
                self.movimiento = int(self.movimiento)
                self.movimiento += 11
                self.vulnerable = 0
                self.ataque = 1
            else:
                self.movimiento = 1

    def Ataque(self):
        if(self.ataque == 1):
            if(pygame.sprite. collide_rect(self.jugador, self) == True):
                self.jugador.Perder_vida()

    def update(self):
        self.Movimiento()
        self.Ataque()
            
        

class Bala(pygame.sprite.Sprite):
    def __init__(self, pos, direccion):
        pygame.sprite.Sprite.__init__(self)
        if(direccion == "derecha"):
            self.image = pygame.image.load("jugador/bala_der.png").convert_alpha()
            self.rect = self.image.get_rect()
            self.rect.bottom = pos.rect.bottom - 8
            self.rect.right = pos.rect.right
        if(direccion == "izquierda"):
            self.image = pygame.image.load("jugador/bala_izq.png").convert_alpha()
            self.rect = self.image.get_rect()
            self.rect.bottom = pos.rect.bottom - 8
            self.rect.left = pos.rect.left
        self.direccion = direccion
        self.recorrido = 0
        self.todos = pos.todos
        self.enemigos = pos.enemigos
        self.jugador = pos

    def Movimiento(self):
        if(self.direccion == "derecha"):
            self.rect.x += 5
        if(self.direccion == "izquierda"):
            self.rect.x += -5
        self.recorrido += 5
        if(self.recorrido >= 250):
            self.todos.remove(self)

    def Colicion(self):
        colicion = pygame.sprite.spritecollide(self, self.enemigos, False)
        for i in colicion:
            if(i.vulnerable == 1):
                self.enemigos.remove(i)
                self.todos.remove(i)
                self.jugador.puntaje += 100
            else:
                self.todos.remove(self)
        

    def update(self):
        self.Movimiento()
        self.Colicion()

class Jugador(pygame.sprite.Sprite):

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("jugador/quieto_der.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.tam_x , self.tam_y = self.image.get_size()
        self.rect.x = 51
        self.rect.y = 428 - self.tam_y - 4
        self.movimiento = 0
        self.direccion = None
        self.direccion_imagenes = "derecha"
        self.plataformas = None
        self.velocidad = 5
        self.salto=0
        self.golpe = 0
        self.disparo = 0
        self.todos = None
        self.enemigos = None
        self.vida = 3
        self.regresar = 0
        self.sonido = pygame.mixer.Sound("jugador/disparo.wav")
        self.puntaje = 0

        

    def num_movimiento(self):
        if(self.movimiento == 9):
            self.movimiento = 1

    def Movimiento(self):
        if(self.Coliciones_x()):
            temp_x = self.rect.x
            temp_y = self.rect.bottom
            imagen = None
            self.movimiento = str(self.movimiento)
            if(self.direccion == "derecha"):
                imagen = "jugador/mover_"+self.movimiento+"_der.png"
                temp_x += self.velocidad
                self.direccion_imagenes = self.direccion
                self.image = pygame.image.load(imagen).convert_alpha()
            if(self.direccion == "izquierda"):
                imagen = "jugador/mover_"+self.movimiento+"_izq.png"
                temp_x += -self.velocidad
                self.direccion_imagenes = self.direccion
                self.image = pygame.image.load(imagen).convert_alpha()
            self.rect = self.image.get_rect()
            self.tam_x , self.tam_y = self.image.get_size()
            self.rect.x = temp_x
            self.rect.bottom = temp_y
            self.movimiento = int(self.movimiento)
            self.movimiento += 1
            self.num_movimiento()

    def Quieto(self):
        temp_y = self.rect.bottom
        imagen = None
        if(self.direccion_imagenes == "derecha"):
            temp_x = self.rect.left
            imagen = "jugador/quieto_der.png"
            self.rect = self.image.get_rect()
            self.rect.left = temp_x
        if(self.direccion_imagenes == "izquierda"):
            temp_x = self.rect.right
            imagen = "jugador/quieto_izq.png"
            self.rect = self.image.get_rect()
            self.rect.right = temp_x
        self.image = pygame.image.load(imagen).convert_alpha()
        self.tam_x , self.tam_y = self.image.get_size()
        self.rect.bottom = temp_y
        self.direccion = None
        self.movimiento = 1

    def Caida(self):
        if(self.Coliciones_y() == True):
            temp_x = self.rect.x
            temp_y = self.rect.bottom
            if(self.direccion_imagenes == "derecha"):
                self.image = pygame.image.load("jugador/salto_3_der.png").convert_alpha()
            if(self.direccion_imagenes == "izquierda"):
                self.image = pygame.image.load("jugador/salto_3_izq.png").convert_alpha()
            self.rect = self.image.get_rect()
            self.tam_x , self.tam_y = self.image.get_size()
            self.rect.x = temp_x
            self.rect.bottom = temp_y
            pygame.time.wait(10)
            self.rect.bottom += 4
        if(self.rect.top > 600):
            self.Perder_vida()
            

    def Coliciones_x(self):
        colicion = pygame.sprite.spritecollide(self, self.plataformas, False)
        coliciones = True
        for i in colicion:
            if self.rect.bottom > i.rect.top:
                if(self.direccion == "izquierda"):
                    if pygame.sprite.collide_rect(self, i):
                        colicones = False
                        if ((i.rect.right - self.rect.left) <= 10):
                            self.rect.left += i.rect.right - self.rect.left + 1
                if(self.direccion == "derecha"):
                    if pygame.sprite.collide_rect(i, self):
                        colicones = False
                        if((self.rect.right - i.rect.left) <= 10):
                            self.rect.right -= self.rect.right - i.rect.left - 1
        return coliciones

    def Coliciones_y(self):
        caida = False
        if(self.salto == 0):
            caida = True
            for i in self.plataformas:
                if((self.rect.left <= i.rect.right) and (self.rect.right >= i.rect.left)):
                    if(((self.rect.bottom - i.rect.top) >= 0) and ((self.rect.bottom - i.rect.top) <= 5)):
                        caida = False
                        return caida
                    else:
                        caida = True
                        return caida
            return caida
        return caida


    def Perder_vida(self):
        if(self.vida == 0):
            self.todos.remove(self)
        else:
            self.vida += -1
            self.rect.x = 51
            self.rect.y = 428 - self.tam_y - 4

    def Salto(self):
        if(self.salto < 15 and self.salto > 0):
            temp_x = self.rect.x
            temp_y = self.rect.bottom
            if(self.direccion_imagenes == "derecha"):
                self.image = pygame.image.load("jugador/salto_2_der.png").convert_alpha()
            if(self.direccion_imagenes == "izquierda"):
                self.image = pygame.image.load("jugador/salto_2_izq.png").convert_alpha()
            self.rect = self.image.get_rect()
            self.tam_x , self.tam_y = self.image.get_size()
            self.rect.x = temp_x
            self.rect.bottom = temp_y
            pygame.time.wait(10)
            self.rect.bottom -= 4
            self.salto += 1
        else:
            self.salto = 0

    def Mover_pantalla(self, lista):
        if(self.rect.right >= 700):
            for i in lista:
                self.regresar += 1
                i.rect.right += -700
            return -700
        return 0


    def Disparo(self):
        if(self.disparo < 14 and self.disparo > 0):
            temp_y = self.rect.bottom
            imagen = None
            self.disparo = str(self.disparo)
            if(self.direccion_imagenes == "derecha"):
                temp_x = self.rect.left
                self.image = pygame.image.load("jugador/disparo_" + self.disparo + "_der.png").convert_alpha()
                self.rect = self.image.get_rect()
                self.rect.left = temp_x
            if(self.direccion_imagenes == "izquierda"):
                temp_x = self.rect.right
                self.image = pygame.image.load("jugador/disparo_" + self.disparo + "_izq.png").convert_alpha()
                self.rect = self.image.get_rect()
                self.rect.right = temp_x
            self.tam_x , self.tam_y = self.image.get_size()
            self.rect.bottom = temp_y
            pygame.time.wait(10)
            self.disparo = int(self.disparo)
            if(self.disparo == 2):
                self.sonido.play()
            if(self.disparo == 8):
                bala = Bala(self, self.direccion_imagenes)
                self.todos.add(bala)
            self.disparo += 1
        else:
            self.disparo = 0
            
            
        
    def update(self):
        self.Movimiento()
        self.Caida()
        self.Salto()
        self.Disparo()
        
        
class MENU:
    """Representa un menu con opciones para un juego"""
    
    def __init__(self, opciones, colores):
        self.opciones = opciones
        self.colores=colores
        self.font = pygame.font.Font('dejavu.ttf', 40)
        self.seleccionado = 0
        self.total = len(self.opciones)
        self.mantiene_pulsado = False

    def actualizar(self):
        """Altera el valor de 'self.seleccionado' con los direccionales."""

        k = pygame.key.get_pressed()

        if not self.mantiene_pulsado:
            if k[K_UP]:
                self.seleccionado -= 1
            elif k[K_DOWN]:
                self.seleccionado += 1
            elif k[K_KP_ENTER] or k[K_RETURN]:
                # Invoca a la función asociada a la opción.
                titulo, funcion = self.opciones[self.seleccionado]
                funcion()

        # procura que el cursor esté entre las opciones permitidas
        if self.seleccionado < 0:
            self.seleccionado = 0
        elif self.seleccionado > self.total - 1:
            self.seleccionado = self.total - 1

        # indica si el usuario mantiene pulsada alguna tecla.
        self.mantiene_pulsado = k[K_UP] or k[K_DOWN] or k[K_RETURN] or k[K_KP_ENTER]


    def imprimir(self, screen):
        """Imprime sobre 'screen' el texto de cada opción del menú."""

        total = self.total
        indice = 0
        altura_de_opcion = 50
        x = 105
        y = 105
        
        for (titulo, funcion) in self.opciones:
            if indice == self.seleccionado:
                color = self.colores[0]
            else:
                color = self.colores[1]

            imagen = self.font.render(titulo, 1, color)
            posicion = (x, y + altura_de_opcion * indice)
            indice += 1
            screen.blit(imagen, posicion)


