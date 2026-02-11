#importamos la libreria de arcade
import arcade
from entities import Jugador 

#definimos el ancho y alto de la ventana donde se mostrara el juego
WIDTH = 1600
HEINGT = 1280
TITULO = "soulslike"

#esta va hacer la clase donde ejecutaros todo nuestro codigo
#arcade.window es una clase predefinida por arcade de donde nosotros podemos hacer el juego 
class Juego(arcade.Window):
    def __init__(self):
        super().__init__(WIDTH, HEINGT, TITULO)
        self.camara = arcade.Camera2D()
        self.tile_map =  None
        self.scene = None

        arcade.set_background_color(arcade.csscolor.CORNFLOWER_BLUE)
    
    def setup(self):
        #aqui lo que hacemos es carfar el mapa arcade ya reconoce el formato .tmx
        self.tile_map = arcade.load_tilemap("assets/nivel_1.tmx", scaling=1)

        #y aqui creamos una esena para cargar todas la capas de nuestro nivel 
        self.scene = arcade.Scene.from_tilemap(self.tile_map)

        #creamos a nuestros personaje 
        self.caballero = Jugador()

        #definimos las coordenadas donde aparecera el personaje esto de acuerdo con el mapa
        self.caballero.center_x = 64
        self.caballero.center_y = 96

        #aja aqui lo que hacemos es que como ya nuestro juegador es un objeto lo colocamos en la esena que ya habiamos predefinido para el mapa
        self.scene.add_sprite("jugador", self.caballero)

        #definimos la gravedad
        gravedad = 0.5

        #ahora creamos una variable para que contega el motor de fisicas de arcade
        self.physics_engine = arcade.PhysicsEnginePlatformer(self.caballero, platforms=self.scene["piso"], gravity_constant=gravedad)

        #aqui mediante la variable que definimos en el construtor podemos hacer zoom para que no se muestre todo el mapa
        self.camara.zoom = 2.0

    def on_draw(self):
        #para limpiar pantalla
        self.clear()

        #primero verificamos que haya una esena 
        if self.scene:
            self.camara.use()
            self.scene.draw()

    def on_update(self, delta_time):
        self.caballero.update_animation(delta_time)
        
        self.camara.position = (self.caballero.center_x, self.caballero.center_y)

        self.physics_engine.update()

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
        
def main():
    window = Juego()
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()