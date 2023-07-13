import pygame
import random

class Enemigo:
    def __init__(self,imagen,x,y,direccion_x,direccion_y,vida,tipo):
        self.imagen = imagen
        self.rect = self.imagen.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.direccion_x = direccion_x
        self.direccion_y = direccion_y
        self.vida = vida
        self.tipo = tipo

def crear_proyectiles(x,y,velocidad,origen):
    imagen_proyectil_marisa = pygame.image.load("segundo_parcial/archivos/proyectil_marisa.png")
    imagen_proyectil_marisa = pygame.transform.scale(imagen_proyectil_marisa,(10,10))
    rect_proyectil_marisa = imagen_proyectil_marisa.get_rect()
    imagen_proyectil_enemigo = pygame.image.load("segundo_parcial/archivos/proyectil_enemigo.png")
    imagen_proyectil_enemigo = pygame.transform.scale(imagen_proyectil_enemigo,(10,10))
    rect_proyectil_enemigo = imagen_proyectil_enemigo.get_rect()
    proyectil = {"velocidad": velocidad,
                "origen": origen}
    if origen == "marisa":
        proyectil["imagen"] = imagen_proyectil_marisa
        proyectil["rect"] = rect_proyectil_marisa.copy()
    elif origen == "enemigo":
        proyectil["imagen"] = imagen_proyectil_enemigo
        proyectil["rect"] = rect_proyectil_enemigo.copy()
    proyectil["rect"].x = x
    proyectil["rect"].y = y
    return proyectil

def mover_proyectiles(lista_proyectiles):
    for proyectil in lista_proyectiles:
        if proyectil['origen'] == 'marisa':
            proyectil['rect'].y -= proyectil['velocidad']
        else:
            proyectil['rect'].y += proyectil['velocidad']

        
def crear_lista_enemigo(cantidad,tipo):
    lista_enemigos = []
    if tipo == 1:
        for i in range(cantidad):
            imagen = pygame.image.load("segundo_parcial/archivos/Enemigo_azul.png")
            imagen = pygame.transform.scale(imagen,(30,30))
            x = 250
            y = 0
            direccion_x = random.choice(["izquierda", "derecha"])
            direccion_y = "abajo"
            vida = 1
            tipo = 1
            enemigo = Enemigo(imagen, x, y, direccion_x, direccion_y,vida,tipo)
            lista_enemigos.append(enemigo)
    elif tipo == 2:
        for i in range(cantidad):
            imagen = pygame.image.load("segundo_parcial/archivos/enemigo_rojo.png")
            imagen = pygame.transform.scale(imagen,(30,30))
            x = 250
            y = 0
            direccion_x = random.choice(["izquierda", "derecha"])
            direccion_y = "abajo"
            vida = 2
            tipo = 2
            enemigo = Enemigo(imagen, x, y,direccion_x, direccion_y,vida,tipo)
            lista_enemigos.append(enemigo)
    return lista_enemigos