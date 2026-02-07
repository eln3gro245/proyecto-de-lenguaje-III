#importamos la libreria de arcade
import arcade 

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

if __name__ == "__main__":
    pass