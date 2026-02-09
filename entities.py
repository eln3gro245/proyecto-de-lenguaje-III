import arcade
from arcade.hitbox import HitBox

class Entities(arcade.Sprite):
    def __init__(self, escala, hp, speed, jump, force):
        super().__init__(scaling=escala)
        #aqui definimos los atributos
        self.hp = hp
        self.speed = speed
        self.jump = jump
        self.force = force
        self.is_climbing = False

    #hacemos un metodo para carga las animaciones que dispone nuestro png
    def cargar_hoja(self, archivo, frames):
        #usamos load_spritesheet que toma ciertos atribitos de nuestro personaje y los framas
        #que pasa nuestra imagen png donde tenemos al personaje esta funcion lo tiene que animar de que manera 
        #y corta en partes todos los frames donde nuestro personje se mueve y lo que hace es que le da vida 
        sheet = arcade.load_spritesheet(file_name=archivo)
        
        
        return sheet.get_texture_grid(size=(80,120), columns=frames, count=frames, )

class Jugador(Entities):
    def __init__(self):
        super().__init__(escala=1, hp=5, speed=5, jump=12, force=15)

        #hago una variable para para buscar mas facil la ruta
        ruta = "assets/Colour1/NoOutline/120x80_PNGSheets/"

        #hacemos un diccionario para almacenar la ruta de los archivos que usaremos para animar nuestro personje
        self.animaciones = {
            "quieto": self.cargar_hoja(f"{ruta}_Idle.png", 10),
            "ataque": self.cargar_hoja(f"{ruta}_Attack.png", 4),
            "salto":  self.cargar_hoja(f"{ruta}_Jump.png", 3),
            "morir":  self.cargar_hoja(f"{ruta}_Death.png", 10)
        }
        
        #esto es para ajustar el marco invicible que tiene el png para que las colisiones sean lo mas precisas que podamos
        self.hit_box = HitBox([(-10, -19), (10, -19), (10, 19), (-10, 19)])

        self.texture = self.animaciones["quieto"][0]
