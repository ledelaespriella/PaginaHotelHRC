from sqlite3.dbapi2 import Error
from formularios import FormLogin,FormRegistro, formHabitaciones
import os
import utils
from flask import Flask, request, flash, session
from flask import render_template
from flask.helpers import url_for
from werkzeug.utils import redirect
import yagmail
import sqlite3

app = Flask(__name__)
app.secret_key = os.urandom(24)

#luis
@app.route('/', methods=['GET'])
def inicio():
    return render_template('Home.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    form= FormLogin()
    if request.method == 'POST':
        user = form.correo.data
        password = form.contrasena.data
        userRequest = None
        passwordRequest = None
        try:
            with sqlite3.connect("HRC.db") as con:
                cur = con.cursor()
                consulta = cur.execute("SELECT email, password, rol, cedula FROM usuarios WHERE email=? and password = ?", [user, password]).fetchone()
                print(consulta)                                                                             
                con.commit()
                userRequest = consulta[0]
                passwordRequest = consulta[1]
                rol = consulta[2]
                cedula = consulta[3]
        except Error: 
            return 'Error al conectar con la base de datos'
        if (user == userRequest and password == passwordRequest):
            session['rol'] = rol
            session['cedula'] = cedula
            print(session)
            if(rol == 'final'):
                print(session['rol'])
                return redirect(url_for("home"))
        else:
            if(user != userRequest):
                flash('Usuario incorrecto')
            elif(password != passwordRequest):
                flash('Verifique la contraseña e intente nuevamente')
            return render_template('login.html',form=form)
    else:
        return render_template('login.html',form=form)



@app.route('/registro', methods=['GET', 'POST'])
def registro():
    form=FormRegistro()
    try:
        if request.method == 'POST':
            primerNombre = form.Primer_nombre.data
            segudoNombre = form.Segundo_nombre.data
            primerApellido = form.Primer_apellido.data
            segudoApellido = form.Segundo_apellido.data
            cedula = form.identificacion.data
            correo = form.correo.data
            passw = form.contrasena.data
            passwVerificacion = form.confirmacion_contrasena.data
            error = None
            rol = 'final'
            if not utils.isEmailValid(correo):
                error = "Correo invalido."
                flash(error)
                return render_template("registro.html")
            if not utils.isPasswordValid(passw):
                error = "Contraseña invalida por favor registre una correcta."
                flash(error)
                return render_template("registro.html",form=form)
            if passw!=passwVerificacion:
                return render_template("registro.html",form=form)
            else:
                try:
                    with sqlite3.connect('HRC.db') as con:
                        cur = con.cursor()
                        cur.execute('INSERT INTO usuarios(cedula, pNombre, sNombre, pApellido, sApellido, email, password, rol) VALUES (?,?,?,?,?,?,?,?)', (cedula, primerNombre, segudoNombre, primerApellido, segudoApellido, correo, passw, rol))
                        con.commit()
                        return '<p>Conexion exitosa</p>'
                except Error:
                        print('Conexion incompletada')
                        return '<p>Conexion no exitosa</p>'
        else:
            return render_template('registro.html',form=form)
    except:
        return render_template('registro.html',form=form)
    # guardar en un diccionario los datos


@app.route('/login/recuperacion', methods=['GET', 'POST'])
def recuperacion(): 
    if request.method == 'POST':
        correo = request.form['correo']
        error=None

        if not utils.isEmailValid(correo):
            error = "Correo invalido."
            flash(error)
            return render_template("recuperacion.html")
        
        if correo == 'luisdelaespriellaj@hotmail.com':
            return redirect(url_for("mensaje"))
        else:
            error = "Correo no existe en la base de datos"
            flash(error)
            return render_template('recuperacion.html')

    else:
        return render_template('recuperacion.html')


@app.route('/login/recuperacion/mensaje', methods=['GET', 'POST'])
def mensaje():
    return render_template('mensaje.html')

#jose

@app.route("/habitaciones", methods=['GET', 'POST'])
def home():
    if request.method == 'GET':
        form = formHabitaciones()
        try:
            with sqlite3.connect("HRC.db") as con:
                con.row_factory = sqlite3.Row 
                cur = con.cursor()
                cur.execute("SELECT * FROM habitacion")
                row = cur.fetchone()
                if row is None:
                    flash("Habitacion no existente")
                return render_template("habitaciones.html",form=form, row=row)
        except Error:
            print(Error)
            return "Error en el método"
    elif request.method == 'POST':
        form = formHabitaciones()
        try:
            with sqlite3.connect("HRC.db") as con:
                con.row_factory = sqlite3.Row 
                cur = con.cursor()
                cur.execute("SELECT * FROM habitacion")
                row = cur.fetchone()
                if row is None:
                    flash("Habitacion no existente")
                return render_template("habitaciones.html",form=form, row=row)
        except Error:
            print(Error)
    else:
        return "Error en el método"

    

@app.route("/habitaciones/get", methods=['GET', 'POST'])
def Habitaciones_get():
    form = formHabitaciones()
    if request.method == 'POST':
        idHabitacion = form.idHabitacion.data
        try:
            with sqlite3.connect("HRC.db") as con:
                con.row_factory = sqlite3.Row
                cur = con.cursor()
                cur.execute("SELECT * FROM habitacion WHERE id = ?", [idHabitacion])
                row = cur.fetchone()
                if row is None:
                    flash("Habitacion no existente")
                return render_template("habitacionesGet.html",form=form, row=row)
        except Error:
            print(Error)
    return "Error en el método"



@app.route("/habitaciones/list", methods=["GET", "POST"])
def Habitaciones_list():
    form = formHabitaciones()
    try:
         with sqlite3.connect("HRC.db") as con:
             con.row_factory = sqlite3.Row 
             cur = con.cursor()
             cur.execute("SELECT * FROM habitacion")
             row = cur.fetchall()
             return render_template("habitacionesList.html",form=form, row=row)
    except  Error:
         print(Error)



@app.route("/habitaciones/disp", methods=['GET', 'POST'])
def Habitaciones_disp():
    form = formHabitaciones()
    if request.method == 'POST':
        estado = form.estado.data
        if estado:
            estado = 1
        else:
            estado = 0
        try:
            with sqlite3.connect("HRC.db") as con:
                con.row_factory = sqlite3.Row 
                cur = con.cursor()
                cur.execute("SELECT * FROM habitacion WHERE  disponibilidad = ?", [estado])
                row = cur.fetchall()
                if row is None:
                    flash("No hay habitaciones disponibles")
                return render_template("habitacionesList.html",form=form, row=row)
        except Error:
            print(Error)
    return "Error en el método"


#rutas de adri

@app.route('/habitaciones/panelAdm', methods=['GET'])
def panelAdm():
    return render_template("panel_adm.html",)

@app.route('/habitaciones/panelAdm/gestionHab', methods=['GET'])
def gestionHab():
    return render_template('habitaciones.html', rol = session['rol'])

@app.route('/habitaciones/panelAdm/gestionHab/agregarH', methods=['GET', 'POST'])
def agregarH():
    if request.method == 'POST':
        nombreHab = request.form['name_hab_add']
        idHab = request.form['id_hab_add']
        descripcion = request.form['descripcion_add']
        disponibilidad = 1
        numCam = request.form['numero_camas_add']
        capacidad= request.form['capacidad_add']
        valor = request.form['valor_add']
        try:
            with sqlite3.connect('HRC.db') as con:
                cur = con.cursor()
                cur.execute('INSERT INTO habitacion(id, nombre, descripcion, disponibilidad, cantCamas, capMax, precio) VALUES (?,?,?,?,?,?,?)', (idHab, nombreHab, descripcion, disponibilidad, numCam, capacidad, valor))
                con.commit()
                return ('<p>Operacion exitosa</p>')
        except sqlite3.Error:
            print (sqlite3.Error)
            return('<p>Error al realizar la operacion</p>')
    return render_template("agregaHab.html")
    

@app.route('/habitaciones/panelAdm/gestionHab/editarH', methods=['GET', 'POST']) 
def editarH():
    rol = session['rol']
    return render_template("editarHab.html", rol = rol)

@app.route('/habitaciones/panelAdm/gestionHab/eliminarH', methods=['GET'])
def eliminarH():
    admin="admin@gmail.com"
    return render_template("eliminar.html",usuario=admin)

#julian
@app.route('/reserva/<idHab>')
def load_reserva(idHab=None):
    try:
        with sqlite3.connect('HRC.db') as con:
            cur = con.execute('SELECT * FROM habitacion WHERE  id = ?', [idHab])
            con.commit()
            row = cur.fetchall()
    except Error:
        return redirect(url_for("home"))
    return render_template('reserva.html', idHab = idHab) 

@app.route('/reserva/mensaje_reserva', methods=["GET", "POST"])
def reserva():
    if request.method == 'POST':
        checkin = request.form['checkin']
        checkout = request.form['checkout']
        nombres = request.form["nombreR"]
        apellido = request.form['apellidosR']
        correo = request.form['emailR']
        telefono = request.form['numeroR']
        preferencia = request.form['preferenciasR']
        check = request.form['typePay']
        cardName = request.form['name-card']
        cardNum = request.form['number-card']
        cvc = request.form['cvc']
        usuario = session['cedula']
        caducidad = request.form['caducidad']
        idHab = request.form['habitacion']
        
        if utils.isEmailValid(correo):
            if checkin == checkout:
                flash('Las fechas de entrada y salida no pueden ser iguales')
                return render_template('reserva.html')
            if check == 'hotel':
                try:
                    with sqlite3.connect('HRC.db') as con:
                        cur = con.cursor()
                        print(checkin + checkout + check + idHab + usuario)
                        cur.execute('INSERT INTO reserva(checkin, checkout, fPago, idhabitacion, cedula) VALUES (?,?,?,?,?)', (checkin, checkout, check, idHab, usuario))
                        con.commit()
                except:
                    return "<h1>Error al realizar la reserva</h1>"

                text =  ("Reserva realizada con exito, su tipo de pago es " + check +
                        "<br> Nos vemos en el hotel el dia " + checkin)
                return text
            elif check == 'tarjeta':
                try:
                    with sqlite3.connect('HRC.db') as con:
                        cur = con.cursor()
                        print(checkin + checkout + check + idHab + usuario)
                        cur.execute('INSERT INTO reserva(checkin, checkout, fPago, idhabitacion, cedula) VALUES (?,?,?,?,?)', (checkin, checkout, check, idHab, usuario))
                        con.commit()
                except:
                    return "<h1>Error al realizar la reserva</h1>"

                text =  ("Reserva realizada con exito, su tipo de pago es " + check +
                        "<br> Nos vemos en el hotel el dia " + checkin)
                return text
        else:
            return "<h1>Error al realizar la reserva</h1>"

#jesus

@app.route('/habitaciones/panelAdm/gestionCom')
def gestionar_usuario():
    return render_template('gestion_comentarios.html')

@app.route("/misHabitaciones")
def mishabitaciones():
    return render_template("gestion_comentarios.html")

if __name__ == '__main__':
    app.run(debug=True, port=8000)
