#importamos la libreria de arcade
import arcade
from conexion import inicializar_base_de_datos, obtener_datos_jugador
from entities import Jugador, Esqueleto

#definimos el ancho y alto de la ventana donde se mostrara el juego
WIDTH = 1600
HEIGHT = 1280
TITULO = "The Hero Knight"

#esta va hacer la clase donde ejecutaros todo nuestro codigo
#arcade.window es una clase predefinida por arcade de donde nosotros podemos hacer el juego 
class Juego(arcade.Window):
    def __init__(self):
        super().__init__(WIDTH, HEIGHT, TITULO)
        self.camara = arcade.Camera2D()
        self.tile_map =  None
        self.scene = None

        self.ronda_actual = 1
        self.max_rondas = 3
        self.spawn_completado = False

        self.nivel_1_complete = False

        self.lista_enemigos = arcade.SpriteList()

        arcade.set_background_color(arcade.csscolor.CORNFLOWER_BLUE)
    
    def setup(self):
        import os  
        
        map_path = "assets/n3/mapa_nivel_2.tmx"
        self.tile_map = arcade.load_tilemap(map_path, scaling=1)

        # Lógica de audio (DEBE tener la misma alineación que la línea de arriba)
        bg_music_path = self.tile_map.properties.get("musica_nivel2")
        
        if bg_music_path:
            # Estas líneas llevan 4 espacios extra a la derecha del 'if'
            sound_file = os.path.basename(str(bg_music_path))
            asset_path = f"assets/n3/{sound_file}"
            
            self.music = arcade.load_sound(asset_path)
            self.player = arcade.play_sound(self.music, volume=0.5, loop=True)
            
        #El Cálculo de las Dimensiones del Mapa
        #En el código original, cargabamos el mapa pero el programa no "sabía" qué tan grande era en píxeles.con este bloque de codigo obtenemos las dimensiones del mapa. Es decir
        # tile_map.width es la cantidad de cuadros (tiles)
        # tile_map.tile_width es el tamaño de cada cuadro en píxeles
        
        self.map_width = self.tile_map.width * self.tile_map.tile_width
        
        self.map_height = self.tile_map.height * self.tile_map.tile_height

        #y aqui creamos una esena para cargar todas la capas de nuestro nivel 
        self.scene = arcade.Scene.from_tilemap(self.tile_map)

        #creamos a nuestros personaje 
        self.caballero = Jugador()

        #definimos las coordenadas donde aparecera el personaje esto de acuerdo con el mapa
        self.caballero.center_x = 80
        self.caballero.center_y = 300

        #definimos a un enemigo
        self.esqueleto = Esqueleto()

        self.esqueleto.center_x = 800
        self.esqueleto.center_y = 600

        #aja aqui lo que hacemos es que como ya nuestro juegador es un objeto lo colocamos en la esena que ya habiamos predefinido para el mapa
        self.scene.add_sprite("jugador", self.caballero)
        

        #definimos la gravedad
        gravedad = 0.5

        #ahora creamos una variable para que contega el motor de fisicas de arcade
        self.physics_engine = arcade.PhysicsEnginePlatformer(self.caballero, platforms=self.scene["piso"], gravity_constant=gravedad)
        self.physics_engine_esqueleto = arcade.PhysicsEnginePlatformer(self.esqueleto, platforms=self.scene["piso"], gravity_constant=gravedad)

        #aqui mediante la variable que definimos en el construtor podemos hacer zoom para que no se muestre todo el mapa
        self.camara.zoom = 2.0

        #lo añadimos a nuestra lista de coliciones
        self.lista_enemigos.append(self.esqueleto)

    def on_draw(self):
        #para limpiar pantalla
        self.clear()

        #primero verificamos que haya una esena 
        if self.scene:
            self.camara.use()
            self.scene.draw()
            self.lista_enemigos.draw()
            

    def on_update(self, delta_time):
        
        self.caballero.update_animation(delta_time)

        self.physics_engine.update()
        self.physics_engine_esqueleto.update()
        
        # 1. Definir hacia dónde queremos que vaya la cámara (el jugador)
        target_x = self.caballero.center_x
        target_y = self.caballero.center_y

        # 2. Limitar para que la cámara no se salga de los bordes del mapa
        # Nota: Dividimos el ancho/alto de la ventana por el zoom para saber qué ve el jugador
        view_width = self.width / self.camara.zoom
        view_height = self.height / self.camara.zoom

        # Clamp asegura que el valor esté entre el mínimo (0 + mitad de vista) 
        # y el máximo (ancho del mapa - mitad de vista)
        final_x = arcade.math.clamp(target_x, view_width / 2, self.map_width - view_width / 2)
        final_y = arcade.math.clamp(target_y, view_height / 2, self.map_height - view_height / 2)

        # 3. Aplicar la posición
        self.camara.position = (final_x, final_y)

        for self.esqueleto in self.lista_enemigos:
            self.esqueleto.pensar(self.caballero)

        for enemigo in self.lista_enemigos:
            if enemigo.invulnerable:
                enemigo.tiempo_invulnerabilidad += delta_time
                if enemigo.tiempo_invulnerabilidad > 1.0: 
                    enemigo.invulnerable = False
                    enemigo.tiempo_invulnerabilidad = 0

        #verificamos las coliciones para realizar el daño
        if self.caballero.estado_actual == "ataque" or self.caballero.estado_actual == "ataque_movimiento" and self.caballero.frame_actual == 2:
            self.caballero.verificar_impacto(self.lista_enemigos)

        # Verificamos si la lista está vacía para pasar de ronda o de nivel
        if len(self.lista_enemigos) == 0:
            if self.ronda_actual < 3:
                self.ronda_actual += 1
                self.spawn_ronda()
                print(f"Iniciando Ronda {self.ronda_actual}")
            else:
                self.nivel_1_complete = True 


        if self.caballero.bottom < 0:
            print("¡Caíste al vacío!")
            self.caballero.hp = 0
            self.caballero.morir() # Llama a tu función de muerte

            # 2. Chequeo para los enemigos (dentro de tu bucle for)
        for self.esqueleto in self.lista_enemigos:
            if self.esqueleto.bottom < 0:
                self.esqueleto.hp = 0
                self.esqueleto.morir()
                

    def on_key_press(self, key, modifiers):
        if key == arcade.key.A or key == arcade.key.LEFT:
            self.caballero.change_x = -self.caballero.speed
        elif key == arcade.key.D or key == arcade.key.RIGHT:
            self.caballero.change_x = self.caballero.speed
        elif key == arcade.key.W or key == arcade.key.SPACE:
            if self.physics_engine.can_jump():
                self.caballero.change_y = self.caballero.jump
        elif key == arcade.key.ENTER:
            self.caballero.ataque()
        

    def on_key_release(self, key, modifiers):
        if key in (arcade.key.A, arcade.key.LEFT, arcade.key.D, arcade.key.RIGHT):
            self.caballero.change_x = 0

    def spawn_ronda(self):
        
        self.esqueleto = Esqueleto()
        # Los ponemos en puntos específicos del mapa_nivel_2
        self.esqueleto.center_x = 1000
        self.esqueleto.center_y = 500
        
        # Sincronizamos con tu lógica de invulnerabilidad corregida
        self.esqueleto.invulnerable = False
        self.esqueleto.tiempo_invulnerabilidad = 0
        
        self.lista_enemigos.append(self.esqueleto)

        
        self.physics_engine_esqueleto = arcade.PhysicsEnginePlatformer(self.esqueleto, platforms=self.scene["piso"], gravity_constant=0.5)

            
        
def main():
    window = Juego()
    window.setup()
    arcade.run()


    
    def main():
    # 1. Inicializamos la base de datos (crea tablas y datos del jugador)
     from conexion import inicializar_base_de_datos, obtener_datos_jugador
    print("--- Verificando Base de Datos ---")
    inicializar_base_de_datos()
    
    # 2. Verificación rápida: ¿La base de datos tiene la defensa (atributo nuevo)?
    datos = obtener_datos_jugador()
    if datos:
        # Según tu entities.py, la defensa debería ser 15.0
        print(f"✔ Datos cargados de DB. Defensa detectada: {datos[5]}")
    
    # 3. Lanzamos el juego
    window = Juego()
    window.setup()
    arcade.run()

if __name__ == "__main__":
    main()