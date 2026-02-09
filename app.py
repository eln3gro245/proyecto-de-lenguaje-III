#importamos la libreria de arcade
import arcade
from entities import Jugador 

#definimos el ancho y alto de la ventana donde se mostrara el juego
ANCHO = 800
ALTO = 600
TITULO = "soulslike"

#esta va hacer la clase donde ejecutaros todo nuestro codigo
#arcade.window es una clase predefinida por arcade de donde nosotros podemos hacer el juego 
class Juego(arcade.Window):
    def __init__(self):
        super().__init__(ANCHO, ALTO, TITULO)
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
        self.caballero.center_x = 400
        self.caballero.center_y = 300

        self.scene.add_sprite("jugador", self.caballero)

    def on_draw(self):
        #para limpiar pantalla
        self.clear()

        #primero verificamos que haya una esena 
        if self.scene: 
            self.scene.draw()
            

def main():
    window = Juego()
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()