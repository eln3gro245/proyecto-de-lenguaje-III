import arcade
import pathlib

arcade.load_font("assets/fonts/Almendra-Bold.ttf")

# Dimensiones 
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
SCREEN_TITLE = "The Hero Knight"

# AssetsPATH
ASSETS_PATH = pathlib.Path(__file__).resolve().parent / "assets"

class MenuView(arcade.View):
    def __init__(self) -> None:
        super().__init__()
        # Cargamos la imagen
        title_image_path = ASSETS_PATH / "images" / "Menu_Principal.png"
        self.title_image = arcade.load_texture(title_image_path)
        #Cargamos la musica
        self.music = arcade.load_sound(ASSETS_PATH / "sounds" / "Soundtrack_Menu.mp3")
        self.player = arcade.play_sound(self.music, volume=0.5, loop=True)
   
    def on_draw(self):
        self.clear()
        
        arcade.draw_texture_rect(
            texture=self.title_image,
            rect=arcade.rect.LBWH(0,0,1280,720),
        ) 
        
        arcade.draw_text(
            "Presiona ENTER para iniciar",
            x=640,
            y=150,
            color=arcade.color.RED_DEVIL,
            font_size=24,
            anchor_x="center",
            font_name="Almendra",
        )

    def on_show_view(self):
        arcade.set_background_color(arcade.color.BLACK)
    
    def on_key_press(self, key, modifiers):
        if key == arcade.key.ENTER:
            select_view = SelectMenuView(self.player)
            self.window.show_view(select_view)
   
   
class SelectMenuView(arcade.View):
    def __init__(self,player_activo):
        super().__init__()
        
        self.background_select = arcade.load_texture(ASSETS_PATH / "images" / "Menu_Inicio.png")
        self.selection = 0
        self.options = ["Crear Partida", "Cargar Partida"]

        self.music_player = player_activo
        
    def on_draw(self):
        self.clear()
        arcade.draw_texture_rect(
            texture=self.background_select,
            rect=arcade.rect.LBWH(0,0,1280,720),
        )

        for i, option in enumerate(self.options):
            color = (165,28,28) if i == self.selection else arcade.color.WHITE
            
            arcade.draw_text(
                option,
                x=100,
                y=400 - (i * 100),
                color=color,
                font_size=35,
                font_name="Almendra",
                anchor_x="left",
            )
            
    def on_key_press(self, symbol, modifiers):
        if symbol == arcade.key.UP:
            self.selection = 0
        elif symbol == arcade.key.DOWN:
            self.selection = 1
        elif symbol == arcade.key.ENTER:
            if self.selection == 0:
                print("Crear Partida seleccionada")
            else:
                print("Cargar Partida seleccionada")

   
def main():
    window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    menu_view = MenuView()
    window.show_view(menu_view)
    arcade.run()

if __name__ == "__main__":
    main()