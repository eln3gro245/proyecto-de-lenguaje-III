import sqlite3

def obtener_datos_jugador():
    
    try:
        #conectamos el archivo creado
        conexion = sqlite3.connect('Database/juego.db')
        
        #- Creamos una variable llamada "conexion" que representa la conexion a la base de datos SQLite.
        
        #- Se usa el metodo ".cursor()" para que cree un objeto cursor que permitira ejecutar las consulta y procesar el resultado.
        
        cursor = conexion.cursor()
        
        #despues se buscan los datos del 'jugador' que inserté en la tabla Entities
        query = "SELECT escala, hp, speed, jump, force FROM Entities WHERE nombre = 'Jugador'"
        
        #- Se utiliza el metodo ".execute()" para enviar la consulta SQL al motor de la base de datos a traves del objeto cursor, dicho metodo toma como argumento una cadena de texto y despues se encarga de ejecutar de la consulta (el query) al motor de la base de datos a traves del cursor 
        
        cursor.execute(query)
        
        #creamos una variable llamada "datos" que contenga el objeto cursor junto con un metodo llamado ".fetchone()", dicho metodo dara el resultado de la consulta (el query) ejecutada peviamente a traves del cursor.
        
        datos = cursor.fetchone()
        
        # Ahora para cerrar la conexion con la base de datos de utiliza el metodo ".close()" con la variable "conexion" que cree antes
        
        conexion.close()
        
        return datos #esto devuelve los datos predeterminados "(1.0, 5, 5.0, 12.0, 15.0)"de los campos

        # y por ultimo un bloque de manejo de excepciones, el cual ayudara a "capturar" cualquier error que pueda ocurrir al conectarse a la base de datos, si ocurre una excepcion, se imprime un mensaje de error. 
        
    except Exception as e:
        print(f"Error al conectar con la base de datos: {e}")
        
        # Si no se devuelven los datos del jugador, la funcion devuelve None
        
        return None
    
# Prueba rápida de conexión
datos = obtener_datos_jugador()

if datos:
    print(f"¡Conexión exitosa! Datos del caballero: {datos}")
else:
    print("No se encontraron datos en la base de datos.")
    
    
    
    
    