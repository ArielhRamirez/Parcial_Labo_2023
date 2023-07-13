from constantes import *
import sqlite3
import elementos
import random
import pygame
pygame.init()
pygame.mixer.init()

class Pantalla_menu:
    def __init__(self):
        self.pantalla = pantalla
        self.rect_juego = rectangulos_menu["juego"]
        self.rect_puntajes = rectangulos_menu["puntajes"]
        self.imagen_fondo = imagen_fondo_menu
        self.fuente_letra = ruta_de_fuente
        self.sonido_fondo = sonido_fondo_menu
        self.sonido_fondo.set_volume(0.05)
        self.rect_juego_armado = pygame.Rect(self.rect_juego["pos_x"], self.rect_juego["pos_y"], self.rect_juego["ancho"], self.rect_juego["alto"])
        self.rect_puntajes_armado = pygame.Rect(self.rect_puntajes["pos_x"], self.rect_puntajes["pos_y"], self.rect_puntajes["ancho"], self.rect_puntajes["alto"])
        self.active = True
        self.flag_correr = self.active
        
    def mostrar(self):
        while self.flag_correr:
            self.sonido_fondo.play(-1)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    juego_rect = pygame.Rect(self.rect_juego_armado)
                    puntajes_rect = pygame.Rect(self.rect_puntajes_armado)
                    if juego_rect.collidepoint(event.pos):
                        self.active = False
                        self.flag_correr = self.active
                        self.sonido_fondo.stop()
                        cambiar_pantalla_activa(pantallas, "juego")

                    elif puntajes_rect.collidepoint(event.pos):
                        self.active = False
                        self.flag_correr = self.active
                        self.sonido_fondo.stop()
                        cambiar_pantalla_activa(pantallas, "puntajes")
                     
            pygame.draw.rect(self.pantalla, colores.WHITE, self.rect_juego_armado)
            pygame.draw.rect(self.pantalla, colores.WHITE, self.rect_puntajes_armado)


            self.pantalla.blit(self.imagen_fondo, (0, 0))
            self.pantalla.blit(texto_de_titulo, (45, 5))
            self.pantalla.blit(texto_de_juego, (335, 200))
            self.pantalla.blit(texto_de_puntaje, (305, 303))
            pygame.display.flip()
            
class Pantalla_game_over:
    def __init__(self):
        self.pantalla = pantalla
        self.imagen_fondo = imagen_fondo_over
        self.sonido_fondo = sonido_fondo_over
        self.sonido_fondo.set_volume(0.07)
        self.active = False
        self.nombre_ingresado = ""
        self.flag_correr = self.active
        
    def mostrar(self,score):
        self.sonido_fondo.play(0)
        puntaje_redondeado = round(score)
        while self.flag_correr:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        if len(self.nombre_ingresado) >= 1:
                            self.active = False
                            self.flag_correr = self.active
                            self.sonido_fondo.stop()
                            with sqlite3.connect("ranking.db") as conexion:
                                conexion.execute("INSERT INTO puntajes(nombre, puntaje) VALUES (?, ?)", (self.nombre_ingresado, puntaje_redondeado))
                                conexion.commit()
                            pantalla_juego.reiniciar()
                            self.nombre_ingresado = ""
                            cambiar_pantalla_activa(pantallas, "puntajes")
                    elif event.key == pygame.K_BACKSPACE:
                        self.nombre_ingresado = self.nombre_ingresado[:-1]
                    else:
                        self.nombre_ingresado += event.unicode
            pantalla.blit(self.imagen_fondo,(0,0))
            pygame.draw.rect(self.pantalla, (colores.WHITE), rect, 2)
            texto_nombre_ingresado = fuente_tres.render(self.nombre_ingresado, True, (colores.WHITE))
            pantalla.blit(texto_over, (255,100))
            pantalla.blit(texto_ingrese,(240,250))
            pantalla.blit(texto_nombre_ingresado, (rect.x + 5, rect.y + 5))
            pygame.display.flip()
            
class Pantalla_puntajes:
    def __init__(self):
        self.pantalla = pantalla
        self.imagen_fondo = imagen_fondo_puntajes
        self.active = False
        self.flag_correr = self.active
        
    def mostrar(self):
        while self.flag_correr:
            self.pantalla.blit(self.imagen_fondo,(0,0))
            self.pantalla.blit(texto_ranking, (360, 40))
            self.pantalla.blit(texto_encabezado_nombre, (300, 100))
            self.pantalla.blit(texto_encabezado_puntaje, (500, 100))
            with sqlite3.connect("ranking.db") as conexion:
                cursor = conexion.execute("SELECT nombre, puntaje FROM puntajes ORDER BY puntaje DESC LIMIT 10")
                ranking = cursor.fetchall()

            y = 150
            for i, (nombre, puntaje) in enumerate(ranking):
                texto_nombre = fuente_nombre.render(f"{i + 1}. {nombre}", True, colores.WHITE)
                texto_puntaje = fuente_puntaje.render(str(puntaje), True, colores.WHITE)
                self.pantalla.blit(texto_nombre, (300, y))
                self.pantalla.blit(texto_puntaje, (500, y))
                y += 30
            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        self.active = False
                        self.flag_correr = self.active
                        cambiar_pantalla_activa(pantallas,"menu")

class Pantalla_juego:
    def __init__(self):
        self.pantalla = pantalla
        self.score = 0
        self.vidas_marisa = 3
        self.rect_marisa = pygame.Rect(235, 400, 30, 45)
        self.lista_proyectiles = []
        self.lista_enemigos = []
        self.marisa_mov_x = 0
        self.marisa_mov_y = 0
        self.vida_enemigo = 2
        self.imagen_marisa = imagen_marisa
        self.imagen_marisa_izquierda = imagen_marisa_izquierda
        self.imagen_marisa_derecha = imagen_marisa_derecha
        self.imagen_actual = imagen_marisa
        self.cantidad_enemigos = elementos.crear_lista_enemigo(1,1)
        self.temporizador = 60
        self.minimo_de_enemigos = 8
        self.imagen_fondo = imagen_fondo_juego
        self.clock = pygame.time.Clock()
        self.sonido_fondo = sonido_fondo_juego
        self.flag_correr = True
        self.active = False
        self.flag_correr = self.active
        with sqlite3.connect("ranking.db") as conexion:
                        sentencia = ''' create table if not exists puntajes
                        (
                        id integer primary key autoincrement,
                        nombre text,
                        puntaje INTEGER
                        )
                        '''
                        conexion.execute(sentencia)
    def reiniciar(self):
        self.score = 0
        self.vidas_marisa = 3
        self.temporizador = 60
        self.rect_marisa = pygame.Rect(235, 400, 30, 45)
        self.lista_proyectiles = []
        self.lista_enemigos = []
                        
    def actualizar_pantalla(self):
        for proyectil in self.lista_proyectiles:
            if proyectil['origen'] == 'marisa':
                for enemigo in self.lista_enemigos:
                    if enemigo.tipo == 1:
                        if proyectil['rect'].colliderect(enemigo.rect):
                            enemigo.vida -= 1
                            if proyectil in self.lista_proyectiles:
                                self.lista_proyectiles.remove(proyectil)
                            if enemigo.vida <= 0:
                                self.score += 100
                                if enemigo in self.lista_enemigos:
                                    self.lista_enemigos.remove(enemigo)
                    else:
                        if proyectil['rect'].colliderect(enemigo.rect):
                            enemigo.vida -= 1
                            if proyectil in self.lista_proyectiles:
                                self.lista_proyectiles.remove(proyectil)
                            if enemigo.vida <= 0:
                                self.score += 300
                                if enemigo in self.lista_enemigos:
                                    self.lista_enemigos.remove(enemigo)
            elif proyectil["origen"] == "enemigo":
                if proyectil["rect"].colliderect(self.rect_marisa):
                    if self.vidas_marisa > 0:
                        self.vidas_marisa -= 1
                        if proyectil in self.lista_proyectiles:
                            self.lista_proyectiles.remove(proyectil)
        texto_vidas = fuente_juego.render("Vidas: {0}".format(self.vidas_marisa), True, colores.WHITE)
        texto_score = fuente_juego.render("Score: {0}".format(self.score), True, colores.WHITE)
        texto_tiempo = fuente_juego.render("Tiempo: {0}".format(self.temporizador), True, colores.WHITE)
        self.pantalla.blit(texto_vidas, (10, 40))
        self.pantalla.blit(texto_score, (10, 10))
        self.pantalla.blit(texto_tiempo, (10, 70))
        for enemigo in self.lista_enemigos:
            self.pantalla.blit(enemigo.imagen, enemigo.rect)
        for proyectil in self.lista_proyectiles:
            self.pantalla.blit(proyectil['imagen'], proyectil['rect'])
        
    def mostrar(self):
        while self.flag_correr:
            self.sonido_fondo.play(-1)
            lista_eventos = pygame.event.get()
            for evento in lista_eventos:
                if evento.type == pygame.QUIT:
                    self.flag_correr = False

                lista_teclas = pygame.key.get_pressed()
                if lista_teclas[pygame.K_RIGHT] and not lista_teclas[pygame.K_LEFT]:
                    if lista_teclas[pygame.K_LSHIFT]:
                        self.marisa_mov_x = 1
                    else:
                        self.marisa_mov_x = 5
                    self.imagen_actual = self.imagen_marisa_derecha
                elif lista_teclas[pygame.K_LEFT] and not lista_teclas[pygame.K_RIGHT]:
                    if lista_teclas[pygame.K_LSHIFT]:
                        self.marisa_mov_x = -1
                    else:
                        self.marisa_mov_x = -5
                    self.imagen_actual = self.imagen_marisa_izquierda
                else:
                    self.marisa_mov_x = 0
                    self.imagen_actual = self.imagen_marisa
                if lista_teclas[pygame.K_UP] and not lista_teclas[pygame.K_DOWN]:
                    if lista_teclas[pygame.K_LSHIFT]:
                        self.marisa_mov_y = -1
                    else:
                        self.marisa_mov_y = -5
                elif lista_teclas[pygame.K_DOWN] and not lista_teclas[pygame.K_UP]:
                    if lista_teclas[pygame.K_LSHIFT]:
                        self.marisa_mov_y = 1
                    else:
                        self.marisa_mov_y = 5
                else:
                    self.marisa_mov_y = 0
                if lista_teclas[pygame.K_LEFT] and not lista_teclas[pygame.K_RIGHT]:
                    if lista_teclas[pygame.K_LSHIFT]:
                        self.marisa_mov_x = -1
                    else:
                        self.marisa_mov_x = -5
                if evento.type == pygame.KEYDOWN and evento.key == pygame.K_z:
                        proyectil = elementos.crear_proyectiles(self.rect_marisa.x, self.rect_marisa.y, 5,"marisa")
                        self.lista_proyectiles.append(proyectil)
                    
                if evento.type == pygame.USEREVENT:
                    if evento.type == evento_movimiento:
                        for enemigo in self.lista_enemigos:
                            enemigo.direccion_x = random.choice(["izquierda", "derecha"])
                            enemigo.direccion_y = random.choice(["abajo", "arriba"])
                    if evento.type == evento_generacion_proyectiles:
                        for enemigo in self.lista_enemigos:
                            if random.choice([True,False]):
                                proyectil = elementos.crear_proyectiles(enemigo.rect.x, enemigo.rect.y, 5,"enemigo")
                                self.lista_proyectiles.append(proyectil)
                    if evento.type == evento_temporizador:
                        self.temporizador -= 1
                    if evento.type == evento_generacion_enemigos:
                        if self.score < 1000:
                            if len(self.lista_enemigos) < self.minimo_de_enemigos:
                                cantidad_a_generar = self.minimo_de_enemigos - len(self.lista_enemigos)
                                nuevos_enemigos = elementos.crear_lista_enemigo(cantidad_a_generar,1)
                                self.lista_enemigos.extend(nuevos_enemigos)
                        else:
                            if len(self.lista_enemigos) < self.minimo_de_enemigos:
                                cantidad_a_generar = self.minimo_de_enemigos - len(self.lista_enemigos)
                                nuevos_enemigos = elementos.crear_lista_enemigo(cantidad_a_generar,2)
                                self.lista_enemigos.extend(nuevos_enemigos)
                
            elementos.mover_proyectiles(self.lista_proyectiles)
            
            if self.vidas_marisa < 1 or self.score == 20000 or self.temporizador == 0:
                self.active = False
                self.flag_correr = self.active
                self.sonido_fondo.stop()
                cambiar_pantalla_activa(pantallas, "game_over")
                pantalla_game_over.mostrar(self.score)
                
            for enemigo in self.lista_enemigos:
                if enemigo.rect.x <= 0:
                    enemigo.direccion_x = "derecha"
                elif enemigo.rect.x >= 770:
                    enemigo.direccion_x = "izquierda"
                if enemigo.rect.y <= 0:
                    enemigo.direccion_y = "abajo"
                elif enemigo.rect.y >= 350:
                    enemigo.direccion_y = "arriba"
                    
                if enemigo.direccion_y == "arriba":
                    enemigo.rect.y -= 2
                elif enemigo.direccion_y == "abajo":
                    enemigo.rect.y += 2
                if enemigo.direccion_x == "izquierda":
                    enemigo.rect.x -= 2
                elif enemigo.direccion_x == "derecha":
                    enemigo.rect.x += 2
            
            self.rect_marisa.y += self.marisa_mov_y
            self.rect_marisa.x += self.marisa_mov_x
            if self.rect_marisa.y < 100:
                self.rect_marisa.y = 400
            if self.rect_marisa.y > 555:
                self.rect_marisa.y = 555
            if self.rect_marisa.x < 0:
                self.rect_marisa.x = 0
            if self.rect_marisa.x > 770:
                self.rect_marisa.x = 770
            self.pantalla.blit(self.imagen_fondo,(0,0))
            self.actualizar_pantalla()

            self.pantalla.blit(self.imagen_actual,self.rect_marisa)

            pygame.display.flip()
            
            self.clock.tick(60)
                
pantalla_menu = Pantalla_menu()
pantalla_juego = Pantalla_juego()
pantalla_puntajes = Pantalla_puntajes()
pantalla_game_over = Pantalla_game_over()

pantallas = [pantalla_menu, pantalla_juego, pantalla_puntajes, pantalla_game_over]

def cambiar_pantalla_activa(pantallas, palabra_clave):
    for pantalla in pantallas:
        if pantalla.__class__.__name__ == "Pantalla_" + palabra_clave:
            pantalla.active = True
            pantalla.flag_correr = True
        else:
            pantalla.active = False
            pantalla.flag_correr = False

def mostrar_pantalla_activa(pantallas):
    for pantalla in pantallas:
        if pantalla.active:
            pantalla.mostrar()
            break


while True:
    mostrar_pantalla_activa(pantallas)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()