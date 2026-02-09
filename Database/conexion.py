import sqlite3

def obtener_datos_jugador():
    
    try:
        #conectamos el archivo creado
        conexion = sqlite3.connect('Database/juego.db')
        
        cursor = conexion.cursor()
        
        #despues se buscan los datos del 'jugador' que inserte en la tabla Entities
        query = "SELECT escala, hp, speed, jump, force FROM Entities WHERE nombre = 'Jugador'"
        
        cursor.execute(query)
        
        datos = cursor.fetchone()
        
        conexion.close()
        
        return datos #esto devuelve los datos predeterminados "(1.0, 5, 5.0, 12.0, 15.0)"de los campos

    except Exception as e:
        print(f"Error al conectar con la base de datos: {e}")
        
        return None