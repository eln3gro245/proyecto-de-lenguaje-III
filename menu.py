import arcade 

#hacemos solo el menu que se va a cargar en el app
class Menu(arcade.View):
    def __init__(self):
        super().__init__()

        #hacemos una lista donde estara las opciones del menu
        self.opciones = ["jugar", "salir"]
        self.selecionador = 0

    #definimos el fondo de momento(la idea seria poner una imagen sobre el juego)
    def on_show_view(self):
        arcade.set_background_color(arcade.color.DARK_BLUE)

    def on_draw(self):
        self.clear()

        #definimos la estructura del titulo
        arcade.draw_text(
            "The mystery of the chalice of life",
            self.window.width / 2,
            self.window.height / 2,
            arcade.color.WHITE,
            font_size=40,
            anchor_x="center"
        )# esta es la cofiguracion que tendra el titulo del juego

        #ahora dibijamos las opciones del menu
        for i, opciones in enumerate(self.opciones):
            #coloreamos la opcion de un color amarillo el boton que se este seleccionando
            if i == self.selecionador:
                color = arcade.color.YELLOW
                texto = f"> {opciones} <"
            else:
                arcade.color.GRAY
                texto = opciones

            arcade.draw_text(
                texto,
                self.window.width / 2,
                (self.window.height / 2) - (i * 40),
                color,
                font_size=20,
                anchor_x="center"
            )