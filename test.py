import sqlite3
from sqlite3 import Error

try:
    with sqlite3.connect('HRC.db') as con:
        cur = con.cursor()
        cur.execute('INSERT INTO reserva(checkin, checkout, email, telefono, preferencias, fPago, idHabitacion, cedula) VALUES(?,?,?,?,?,?,?,?)', ['22-05-20', '21-01-20', "correo," "telefono", "preferencia", "check", "idHab", "cedula"])
        con.commit()
except Error:
    print("<h1>Error al realizar la conexion</h1>")