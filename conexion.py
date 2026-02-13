import sqlite3
import os

# 1. Configuración de Rutas
DB_FOLDER = "Database"
DB_PATH = os.path.join(DB_FOLDER, "juego.db")

def conectar():
    """Establece conexión y asegura que la carpeta exista."""
    if not os.path.exists(DB_FOLDER):
        os.makedirs(DB_FOLDER)
    
    try:
        conexion = sqlite3.connect(DB_PATH)
        conexion.execute("PRAGMA foreign_keys = ON")
        return conexion
    except Exception as e:
        print(f"❌ Error de conexión: {e}")
        return None

def inicializar_base_de_datos():
    """Crea las tablas según la estructura de entities.py"""
    conexion = conectar()
    if not conexion:
        return

    cursor = conexion.cursor()

    # Tabla de Items (Catálogo de pociones y objetos)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS items (
            id_item INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL UNIQUE,
            descripcion TEXT,
            valor INTEGER
        )
    ''')

    # Tabla de Inventario
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS inventario (
            id_inv INTEGER PRIMARY KEY AUTOINCREMENT,
            id_item INTEGER,
            cantidad INTEGER DEFAULT 1,
            FOREIGN KEY (id_item) REFERENCES items (id_item)
        )
    ''')

    # Tabla de Datos del Jugador (Coincide con clase Jugador en entities.py)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS datos_jugador (
            id INTEGER PRIMARY KEY CHECK (id = 1),
            nombre TEXT DEFAULT 'Jugador',
            escala REAL,
            hp INTEGER,
            speed REAL,
            jump REAL,
            force REAL,
            defense REAL
        )
    ''')

    # Insertar datos iniciales del Jugador si no existen
    cursor.execute("SELECT COUNT(*) FROM datos_jugador")
    if cursor.fetchone()[0] == 0:
        # Stats extraídos de tu clase Jugador: escala=1, hp=5, speed=5, jump=12, force=10, defense=15
        cursor.execute('''
            INSERT INTO datos_jugador (id, escala, hp, speed, jump, force, defense)
            VALUES (1, 1.0, 5, 5.0, 12.0, 10.0, 15.0)
        ''')
        
    # Insertar pociones predeterminadas en el catálogo si no están
    pociones = [
        ('Poción Verde', 'Aumenta la defensa en +7', 7),
        ('Poción Amarilla', 'Restaura la vida en +6', 6)
    ]
    cursor.executemany('''
        INSERT OR IGNORE INTO items (nombre, descripcion, valor) 
        VALUES (?, ?, ?)
    ''', pociones)

    conexion.commit()
    conexion.close()
    print("✅ Base de datos sincronizada con Entities.")

def obtener_datos_jugador():
    """Recupera los stats para la clase Jugador."""
    conexion = conectar()
    if not conexion:
        return None
        
    cursor = conexion.cursor()
    try:
        cursor.execute("SELECT escala, hp, speed, jump, force, defense FROM datos_jugador WHERE id = 1")
        return cursor.fetchone()
    except Exception as e:
        print(f"❌ Error al obtener datos: {e}")
        return None
    finally:
        conexion.close()

def usar_item_en_db(nombre_item):
    """Disminuye la cantidad en el inventario SQL."""
    conexion = conectar()
    if not conexion:
        return False
        
    cursor = conexion.cursor()
    try:
        # Buscamos el item por nombre y restamos 1 a la cantidad en inventario
        cursor.execute('''
            UPDATE inventario 
            SET cantidad = cantidad - 1 
            WHERE id_item = (SELECT id_item FROM items WHERE nombre = ?) 
            AND cantidad > 0
        ''', (nombre_item,))
        
        # Si la cantidad llega a 0, eliminamos el registro del inventario
        cursor.execute('''
            DELETE FROM inventario WHERE cantidad <= 0
        ''')
        
        conexion.commit()
        return True
    except Exception as e:
        print(f"❌ Error al usar ítem: {e}")
        return False
    finally:
        conexion.close()

def guardar_stats_jugador(jugador):
    """Guarda los stats actuales de la instancia Jugador en la DB."""
    conexion = conectar()
    if not conexion:
        return
        
    cursor = conexion.cursor()
    try:
        cursor.execute('''
            UPDATE datos_jugador 
            SET hp = ?, speed = ?, jump = ?, force = ?, defense = ?
            WHERE id = 1
        ''', (jugador.hp, jugador.speed, jugador.jump, jugador.force, jugador.defense))
        conexion.commit()
    except Exception as e:
        print(f"❌ Error al guardar stats: {e}")
    finally:
        conexion.close()