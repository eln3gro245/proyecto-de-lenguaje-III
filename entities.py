import arcade
from arcade.hitbox import HitBox

class Entities(arcade.Sprite):
    def __init__(self, escala, hp, speed, jump, force):
        super().__init__(scaling=escala)
        #aqui definimos los atributos
        self.estado_actual = "quieto"
        self.hp = hp
        self.speed = speed
        self.jump = jump
        self.force = force
        self.is_climbing = False

    #hacemos un metodo para carga las animaciones que dispone nuestro png
    def cargar_hoja(self, archivo, frames):
        #usamos load_spritesheet para cargar el png en este caso 
        sheet = arcade.load_spritesheet(file_name=archivo)
        
        #ahora con ese png le decimos al size que el marco de nuesrto personaje para realizar un corte en el mismo
        #por que se hace de esta manera por el png que estamos usando tiene varios frames donde el personaje con ayuda del motor va a poder moverse 
        #por eso columns y count nosotros le pasamos los frame que tiene cada png por que no todos los png tinen los mismo frames y lo que hace
        #es que realiza un corte gracias al size para dividirlo la imagen para luego poder hacer la carga de las imagen una por una
        return sheet.get_texture_grid(size=(120,80), columns=frames, count=frames, )

class Jugador(Entities):
    def __init__(self):
        super().__init__(escala=1, hp=5, speed=5, jump=12, force=15)

        #hago una variable para para buscar mas facil la ruta
        ruta = "assets/Colour1/NoOutline/120x80_PNGSheets/"

        #hacemos un diccionario para almacenar la ruta de los archivos que usaremos para animar nuestro personje
        self.animaciones = {
            "quieto": self.cargar_hoja(f"{ruta}_Idle.png", 10),
            "caminar": self.cargar_hoja(f"{ruta}_Run.png", 10),
            "ataque": self.cargar_hoja(f"{ruta}_Attack.png", 4),
            "salto":  self.cargar_hoja(f"{ruta}_Jump.png", 3),
            "morir":  self.cargar_hoja(f"{ruta}_Death.png", 10)
        }
        
        #esto es para ajustar el marco invicible que tiene el png para que las colisiones sean lo mas precisas que podamos
        self.hit_box = HitBox([(-19, -10), (19, -10), (19, 10), (-19, 10)])

        #aqui lo que hacemos es que le definimos las imagen de quieto para predeterminadamente para que aparezca el personaje sin movimientos
        self.texture = self.animaciones["quieto"][0]

        self.frame_actual = 0
        self.tiempo_animacion = 0

    def update_animation(self, delta_time = 1 / 60):
        #como nuestro png no tiene una animacion para ir a la izquierda lo que hago es que la atributo scale que es de arcade lo volteo 
        #de forma de espejo para hacer que se cea como el personaje se mueva a la izquierda
        if self.change_x > 0:
            self.width = abs(self.width)
        elif self.change_x < 0:
            self.width = -abs(self.width)
        
        estado = "caminar" if self.change_x != 0 else "quieto"

        if self.estado_actual != estado:
            self.estado_actual = estado
            self.frame_actual = 0
            self.tiempo_animacion = 0

        self.tiempo_animacion += delta_time
        if self.tiempo_animacion > 0.1:
            self.tiempo_animacion = 0
            self.frame_actual += 1

            if self.frame_actual >= len(self.animaciones[self.estado_actual]):
                self.frame_actual = 0

            self.texture = self.animaciones[self.estado_actual][self.frame_actual]
            