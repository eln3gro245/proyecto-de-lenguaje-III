import arcade
from arcade.hitbox import HitBox

class Entities(arcade.Sprite):
    def __init__(self, escala, hp, speed, jump, force, defense, width, height):
        super().__init__(scaling=escala)
        #aqui definimos los atributos
        self.estado_actual = "quieto"
        self.tipo_ataque = ""
        self.animaciones = {}
        self.hp = hp
        self.speed = speed
        self.jump = jump
        self.force = force
        self.defense = defense
        self.is_climbing = False
        self.atacar = False

        #definimos el alto y el ancho de nuestra entidad
        self.width = width
        self.height = height

        #estas son variable que definimos para a la hora de hacer la animaciones tengamos contadores para los frames
        #que tiempo de animacion es mas que todo para calcular el tiempo de ejecucion y las de los frames los cambia para dar la sensacion de movimiento
        self.frame_actual = 0
        self.tiempo_animacion = 0

    def ataque(self):
        if not self.atacar:
            self.atacar = True
            self.frame_actual = 0

        if self.change_x == 0:
            self.tipo_ataque = "ataque"
            self.frame_actual = 0
        elif self.change_x > 0:
            self.tipo_ataque = "ataque_movimiento"
            self.frame_actual = 0

    def verificar_impacto(self):
        reach = 50 * self.scale

        ataque = arcade.SpriteCircle(1, arcade.color.TRANSPARENT_BLACK)
        ataque.center_x = self.center_x + (reach / 2)
        ataque.center_y = self.center_y

        ataque.width = abs(reach)
        ataque.height = self.height

        golpe = arcade.check_for_collision_with_list(ataque,) #nota falta agregar una lista de sprites para esta funcion que lo hare cuando los tenga

        for enemigo in golpe:
            daño = self.force - self.enemigo.defense

            if daño < 0:
                daño = 0
            
            enemigo.hp -= daño

            if enemigo.hp <= 0:
                enemigo.morir()
            

    def morir(self):
        if self.hp <= 0 and self.estado != "morir":
            self.hp = 0
            self.estado = "morir"
            self.frame_actual = 0


    #hacemos un metodo para carga las animaciones que dispone nuestro png
    def cargar_hoja(self, archivo, frames):
        #usamos load_spritesheet para cargar el png en este caso 
        sheet = arcade.load_spritesheet(file_name=archivo)
        
        #ahora con ese png le decimos al size que el marco de nuesrto personaje para realizar un corte en el mismo
        #por que se hace de esta manera por el png que estamos usando tiene varios frames donde el personaje con ayuda del motor va a poder moverse 
        #por eso columns y count nosotros le pasamos los frame que tiene cada png por que no todos los png tinen los mismo frames y lo que hace
        #es que realiza un corte gracias al size para dividirlo la imagen para luego poder hacer la carga de las imagen una por una
        return sheet.get_texture_grid(size=(self.width, self.height), columns=frames, count=frames)
    
    def update_animation(self, delta_time = 1 / 60):
        animacion = self.animaciones.get(self.estado, self.animaciones.get("quieto"))

        if self.frame_actual >= len(animacion):
            self.frame_actual = 0
        #como nuestro png no tiene una animacion para ir a la izquierda lo que hago es que la atributo scale que es de arcade lo volteo 
        #de forma de espejo para hacer que se cea como el personaje se mueva a la izquierda
        if self.change_x > 0:
            self.width = abs(self.width)
        elif self.change_x < 0:
            self.width = -abs(self.width)

        if self.atacar:
            self.estado = self.tipo_ataque
        elif self.change_y != 0:
            self.estado = "salto"
            if self.change_y < 0:
                self.estado = "caida"
        elif self.change_x != 0:
            self.estado = "caminar"
        elif self.change_x == 0:
            self.estado = "quieto"
        
        #aqui lo que hace es cambiar la varianle del constructor por que la viarible que definimos para hacer el cambio de los estados de movimiento
        if self.estado_actual != self.estado:
            self.estado_actual = self.estado
            self.frame_actual = 0
            self.tiempo_animacion = 0

        #aqui calculamos el tiempo en el que ocurren eso cambios de frames de acuerdo a los fps que en este caso solo usaremos 60
        self.tiempo_animacion += delta_time
        if self.atacar:
            if self.tiempo_animacion > 4.0:
                self.tiempo_animacion = 0
                self.frame_actual += 1

        if self.tiempo_animacion > 0.1:
            self.tiempo_animacion = 0
            self.frame_actual += 1

            #y aqui hacemos el llamado del estado al que queremos cambiar de acuerdo a los valores que tengamos en el diccionario
            if self.frame_actual >= len(self.animaciones[self.estado_actual]):
                self.frame_actual = 0

            #y aqui hace el cambio de estado
            self.texture = self.animaciones[self.estado_actual][self.frame_actual]
            if self.atacar:
                self.atacar = False
                self.frame_actual = 0

class Jugador(Entities):
    def __init__(self):
        super().__init__(escala=1, hp=5, speed=5, jump=12, force=10, defense=15, width=120, height=80)

        #hago una variable para para buscar mas facil la ruta
        ruta = "assets/Colour1/NoOutline/120x80_PNGSheets/"

        #hacemos un diccionario para almacenar la ruta de los archivos que usaremos para animar nuestro personje
        self.animaciones = {
            "quieto": self.cargar_hoja(f"{ruta}_Idle.png", 10),
            "giro": self.cargar_hoja(f"{ruta}_TurnAround.png", 3), 
            "caminar": self.cargar_hoja(f"{ruta}_Run.png", 10),
            "ataque": self.cargar_hoja(f"{ruta}_AttackNoMovement.png", 4),
            "ataque_movimiento": self.cargar_hoja(f"{ruta}_Attack.png", 4),
            "salto":  self.cargar_hoja(f"{ruta}_Jump.png", 3),
            "caida": self.cargar_hoja(f"{ruta}_Fall.png", 3),
            "morir":  self.cargar_hoja(f"{ruta}_Death.png", 10)
        }
        
        #esto es para ajustar el marco invicible que tiene el png para que las colisiones sean lo mas precisas que podamos
        self.hit_box = HitBox([(-19, -10), (19, -10), (19, 10), (-19, 10)])

        #aqui lo que hacemos es que le definimos las imagen de quieto para predeterminadamente para que aparezca el personaje sin movimientos
        self.texture = self.animaciones["quieto"][0]        
            
class Slime(Entities):
    def _init_(self):
        
        super()._init_(escala=1, hp=12, speed=3, jump=8, force=16, defense=5)

        ruta_slime = "assets/SlimeCharacter_nyknck/" 
        
        Caminar = [(f"({ruta_slime}walk01.png),({ruta_slime}walko2.png),({ruta_slime}walk03.png),({ruta_slime}walk04.png)")]
        Saltar = [(f"({ruta_slime}Jump01.png),({ruta_slime}Jump02.png),({ruta_slime}Jump03.png),({ruta_slime}Jump04.png),({ruta_slime}Jump05.png),({ruta_slime}Jump06.png),({ruta_slime}Jump07.png),({ruta_slime}Jump08.png),({ruta_slime}Jump09.png)")]
        Quieto = [(f"({ruta_slime}idle01.png),({ruta_slime}idle02.png)")]

        self.animaciones = {
            "caminar": self.cargar_hoja(Caminar),
            "saltar": self.cargar_hoja(Saltar),
            "quieto":self.cargar_hoja(Quieto)    
        }

        self.hit_box = HitBox([(-15, -15), (15, -15), (15, 10), (-15, 10)])

        self.texture = self.animaciones["quieto"][0]
        
        self.hit_box = HitBox([(-15, -15), (15, -15), (15, 10), (-15, 10)])
