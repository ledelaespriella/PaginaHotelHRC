import sqlite3
from sqlite3 import Error

try:
    with sqlite3.connect('HRC.db') as con:
        cur =con.cursor()
        cur.execute('INSERT INTO habitacion(id, nombre, descripcion, disponibilidad, cantCamas, capMax, precio) VALUES '+  (479, 'Suite', 'Lorem', True, 2, 4, 250000) +')')
        print('Conexion completada')
except Error:
        print('Conexion incompletada')
