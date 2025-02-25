#! /usr/bin/env python
# -*- coding: utf-8 -*-
import pilasengine
import random

TIEMPO = 6
fin_de_juego = False

pilas = pilasengine.iniciar()
# Usar un fondo estándar
fondo = pilas.fondos.Volley()

# Añadir un marcador
puntos = pilas.actores.Puntaje(x= -230, y=100, color=pilas.colores.blanco)
puntos.magnitud = 10
# Añadir el conmutador de Sonido
pilas.actores.Sonido()

# Variables y Constantes
#balas_simples=pilas.actores.Bala()
monos = []

# Funciones
def mono_destruido(MiMunicion, monos):
	monos.eliminar()
	MiMunicion.eliminar()
	# Actualizar el marcador con un efecto bonito
	puntos.escala = 1
	# puntos.escala = pilas.interpolar(1, duracion=0.5, tipo='rebote_final')
	puntos.aumentar(1)
	

def crear_mono():
    # Crear un enemigo nuevo
    enemigo = pilas.actores.Mono()
    # Hacer que se aparición sea con un efecto bonito
    ##la escala varíe entre 0,25 y 0,75 (Ojo con el radio de colisión)
    enemigo.escala = .5
    # Dotarle de la habilidad de que explote al ser alcanzado por un disparo
    enemigo.aprender(pilas.habilidades.PuedeExplotar)
    # Situarlo en una posición al azar, no demasiado cerca del jugador
    x = random.randrange(-320, 320)
    y = random.randrange(-240, 240)
    if x >= 0 and x <= 100:
        x = 180
    elif x <= 0 and x >= -100:
        x = -180
    if y >= 0 and y <= 100:
        y = 180
    elif y <= 0 and y >= -100:
        y = -180
    enemigo.x = x
    enemigo.y = y
    # Dotarlo de un movimiento irregular más impredecible
    tipo_interpolacion = ['lineal',
                            'aceleracion_gradual',
                            'desaceleracion_gradual',
                            'rebote_inicial',
                            'rebote_final']
    
    duracion = 1 +random.random()*4
    
    pilas.utils.interpolar(enemigo, 'x', 0, duracion)
    pilas.utils.interpolar(enemigo, 'y', 0, duracion)
    #enemigo.x = pilas.interpolar(0,tiempo,tipo=random.choice(tipo_interpolacion))
    #enemigo.y = pilas.interpolar(0, tiempo,tipo=random.choice(tipo_interpolacion))
    # Añadirlo a la lista de enemigos
    monos.append(enemigo)
    # Permitir la creación de enemigos mientras el juego esté en activo
    if fin_de_juego:
        return False
    else:
        return True

def game_over(torreta, enemigo):
	#cuando termina el juego	
	global fin_de_juego
	enemigo.sonreir()
	torreta.eliminar()
	puntos.eliminar
	pilas.avisar("GAME OVER. Conseguiste %d puntos" % (puntos.obtener()))
	fin_de_juego = True

class MiMunicion(pilasengine.actores.Actor):
	
    def iniciar(self):
        self.imagen = "disparos/bola_amarilla.png"
    
    def actualizar(self):
        self.escala = 3



pilas.actores.vincular(MiMunicion)
bala_simple = pilas.actores.MiMunicion()

# Añadir la torreta del jugador

torreta = pilas.actores.Torreta(enemigos=monos, cuando_elimina_enemigo=mono_destruido, municion_bala_simple = MiMunicion)

pilas.tareas.agregar(1, crear_mono)
#pilas.mundo.agregar_tarea(1, crear_mono) <-- sintaxis vieja


#pilas.colisiones.agregar(monos, bala_simple, mono_destruido)
pilas.colisiones.agregar(torreta,monos, game_over)
# Arrancar el juego
pilas.ejecutar()

