import pygame
import colores
pygame.mixer.init()
pygame.init()
ANCHO_VENTANA = 800
ALTO_VENTANA = 600
pantalla = pygame.display.set_mode((ANCHO_VENTANA, ALTO_VENTANA))
pygame.display.set_caption("Touhou 19")
score = 0
temporizador = 60

#PANTALLA DEL MENU//
imagen_fondo_menu = pygame.image.load("segundo_parcial/archivos/fondo_menu.png")
imagen_fondo_menu = pygame.transform.scale(imagen_fondo_menu,(800,600))
ruta_de_fuente = "segundo_parcial/archivos/SAKURATA.ttf"
sonido_fondo_menu = pygame.mixer.Sound("segundo_parcial/archivos/musica_menu.mp3")
fuente_menu = pygame.font.SysFont("Bells Morten",65)
fuente_titulo = pygame.font.Font(ruta_de_fuente,100)
texto_de_titulo = fuente_titulo.render("Touhou 19", True, colores.WHITE)
texto_de_juego = fuente_menu.render("Jugar", True, colores.RED1)
texto_de_puntaje = fuente_menu.render("Puntajes", True, colores.RED1)
rectangulos_menu = {
    "juego": {
        "pos_x": 300,
        "pos_y": 200,
        "ancho": 200,
        "alto": 50
    },
    "puntajes": {
        "pos_x": 300,
        "pos_y": 300,
        "ancho": 200,
        "alto": 50
    }
}
#//
#PANTALLA DE GAME OVER //
imagen_fondo_over = pygame.image.load("segundo_parcial/archivos/fondo_game_over.png")
imagen_fondo_over = pygame.transform.scale(imagen_fondo_over,(800,600))
sonido_fondo_over = pygame.mixer.Sound("segundo_parcial/archivos/musica_over.mp3")
sonido_fondo_over.set_volume(0.07)
rect = pygame.Rect(300, 300, 200, 40)
fuente_uno = pygame.font.SysFont("Arial", 70)
fuente_dos = pygame.font.SysFont("Arial",30)
fuente_tres = pygame.font.SysFont("Arial",32)
nombre_ingresado = ""
#texto_nombre_ingresado = fuente_tres.render(self.nombre_ingresado, True, (colores.WHITE))
texto_over = fuente_uno.render("Game Over", True, colores.RED1)
texto_ingrese = fuente_dos.render("Por favor ingrese su nombre:", True, colores.WHITE)
#//
#PANTALLA DE PUNTAJES //
fuente_ranking = pygame.font.SysFont("Arial",45)
texto_ranking = fuente_ranking.render("Ranking", True, colores.WHITE)
fuente_nombre = pygame.font.SysFont("Arial", 20)
fuente_puntaje = pygame.font.SysFont("Arial", 20)
imagen_fondo_puntajes = pygame.image.load("segundo_parcial/archivos/fondo_puntaje.png")
imagen_fondo_puntajes = pygame.transform.scale(imagen_fondo_puntajes,(800,600))
texto_encabezado_nombre = fuente_puntaje.render("Nombre", True, colores.WHITE)
texto_encabezado_puntaje = fuente_puntaje.render("Puntaje", True, colores.WHITE)
#//
#PANTALLA DE JUEGO PRINCIPAL//
imagen_marisa = pygame.image.load("segundo_parcial/archivos/marisa.png")
imagen_marisa = pygame.transform.scale(imagen_marisa,(30,45))
imagen_marisa_derecha = pygame.image.load("segundo_parcial/archivos/marisa_derecha.png")
imagen_marisa_derecha = pygame.transform.scale(imagen_marisa_derecha,(30,45))
imagen_marisa_izquierda = pygame.image.load("segundo_parcial/archivos/marisa_izquierda.png")
imagen_marisa_izquierda = pygame.transform.scale(imagen_marisa_izquierda,(30,45))
evento_movimiento = pygame.USEREVENT
evento_generacion_proyectiles = pygame.USEREVENT
evento_movimiento_proyectiles = pygame.USEREVENT
evento_generacion_enemigos = pygame.USEREVENT
evento_temporizador = pygame.USEREVENT
pygame.time.set_timer(evento_temporizador,1000)
pygame.time.set_timer(evento_generacion_enemigos,3000)
pygame.time.set_timer(evento_movimiento_proyectiles,1000)
pygame.time.set_timer(evento_movimiento,1000)
pygame.time.set_timer(evento_generacion_proyectiles,1000)
imagen_fondo_juego = pygame.image.load("segundo_parcial/archivos/fondo_juego.png")
imagen_fondo_juego = pygame.transform.scale(imagen_fondo_juego,(800,600))
sonido_fondo_juego = pygame.mixer.Sound("segundo_parcial/archivos/musica_main.mp3")
sonido_fondo_juego.set_volume(0.07)
fuente_juego = pygame.font.SysFont("Arial", 20)