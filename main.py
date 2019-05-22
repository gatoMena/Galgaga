#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Escrito por Daniel Fuentes B.
# Licencia: X11/MIT license http://www.opensource.org/licenses/mit-license.php
# https://www.pythonmania.net/es/2010/04/07/tutorial-pygame-3-un-videojuego/

# ---------------------------
# Importacion de los módulos
# ---------------------------

import pygame
from pygame.locals import *
import os
import sys

# -----------
# Constantes
# -----------

SCREEN_WIDTH = 900
SCREEN_HEIGHT = 700
IMG_DIR = "imagenes"

# ------------------------------
# Clases y Funciones utilizadas
# ------------------------------


def load_image(nombre, dir_imagen, alpha=False):
    # Encontramos la ruta completa de la imagen
    ruta = os.path.join(dir_imagen, nombre)
    try:
        image = pygame.image.load(ruta)
    except:
        print("Error, no se puede cargar la imagen: " + ruta)
        sys.exit(1)
    # Comprobar si la imagen tiene "canal alpha" (como los png)
    if alpha is True:
        image = image.convert_alpha()
    else:
        image = image.convert()
    return image


# -----------------------------------------------
# Creamos los sprites (clases) de los objetos del juego:


class Enemy(pygame.sprite.Sprite):
    "El alien y su comportamiento en la pantalla"

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = load_image("alien.png", IMG_DIR, alpha=True)
        self.image = pygame.transform.scale(self.image, (50, 50))
        self.rect = self.image.get_rect()
        self.rect.centerx = SCREEN_WIDTH / 2
        self.rect.centery = SCREEN_HEIGHT / 2
        self.speed = [3, 3]

    def update(self):
        if self.rect.left < 0 or self.rect.right > SCREEN_WIDTH:
            self.speed[0] = -self.speed[0]
        if self.rect.top < 0 or self.rect.bottom > SCREEN_HEIGHT:
            self.speed[1] = -self.speed[1]
        self.rect.move_ip((self.speed[0], self.speed[1]))

    def colision(self, objetivo):
        if self.rect.colliderect(objetivo.rect):
            self.speed[0] = -self.speed[0]


class Nave(pygame.sprite.Sprite):
    "Define el comportamiento de las Naves de ambos jugadores"

    def __init__(self ):
        pygame.sprite.Sprite.__init__(self)
        self.image = load_image("Nave.jpg", IMG_DIR, alpha=True)
        self.image = pygame.transform.scale(self.image, (50, 50))
        self.rect = self.image.get_rect()
        self.rect.centerx = SCREEN_WIDTH/2
        self.rect.centery = SCREEN_HEIGHT-50

    def humano(self):
        # Controlar que la Nave no salga de la pantalla
        if self.rect.bottom >= SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT
        elif self.rect.top <= 0:
            self.rect.top = 0


# ------------------------------
# Funcion principal del juego
# ------------------------------


def main():
    pygame.init()
    # creamos la ventana y le indicamos un titulo:
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Ejemplo de un Pong Simple")

    # cargamos los objetos
    fondo = load_image("fondo.jpg", IMG_DIR, alpha=False)
    fondo = pygame.transform.scale(fondo, (SCREEN_WIDTH, SCREEN_HEIGHT))

    alien = Enemy()
    jugador1 = Nave()

    clock = pygame.time.Clock()
    pygame.key.set_repeat(1, 25)  # Activa repeticion de teclas
    pygame.mouse.set_visible(False)

    # el bucle principal del juego
    while True:
        clock.tick(120)
        # Obtenemos la posicon del mouse
        #pos_mouse = pygame.mouse.get_pos()
        #mov_mouse = pygame.mouse.get_rel()

        # Actualizamos los obejos en pantalla
        jugador1.humano()
        alien.update()

        # Comprobamos si colisionan los objetos
        alien.colision(jugador1)

        # Posibles entradas del teclado y mouse
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit(0)
            elif event.type == pygame.KEYDOWN:
                if event.key == K_UP:
                    jugador1.rect.centery -= 15
                elif event.key == K_DOWN:
                    jugador1.rect.centery += 15
                elif event.key == K_RIGHT:
                    jugador1.rect.centerx += 15
                elif event.key == K_LEFT:
                    jugador1.rect.centerx -= 15
                elif event.key == K_ESCAPE:
                    sys.exit(0)
            elif event.type == pygame.KEYUP:
                if event.key == K_UP:
                    jugador1.rect.centery += 0
                elif event.key == K_DOWN:
                    jugador1.rect.centery += 0
                elif event.key == K_LEFT:
                    jugador1.rect.centerx += 0
                elif event.key == K_RIGHT:
                    jugador1.rect.centerx += 0
            # Si el mouse no esta quieto mover la Nave a su posicion
            #elif mov_mouse[1] != 0:
            #    jugador1.rect.centery = pos_mouse[1]

        # actualizamos la pantalla
        screen.blit(fondo, (0, 0))
        screen.blit(alien.image, alien.rect)
        screen.blit(jugador1.image, jugador1.rect)
        pygame.display.flip()


if __name__ == "__main__":
    main()