import re
from sqlite3.dbapi2 import Error, connect
from formularios import FormLogin,FormRegistro, formHabitaciones
import os
import utils
from flask import Flask, request, flash, session, sessions
from flask import render_template
from flask.helpers import url_for
from werkzeug.utils import redirect
from markupsafe import escape
import yagmail
import sqlite3

app = Flask(__name__)
app.secret_key = os.urandom(24)

#----------------------------------------------------------------LUIS---------------------------------------------------
#Esta es la vista del home
@app.route('/', methods=['GET'])
def inicio():
    return render_template('Home.html')

#Este carga la vista de inicio de sesion
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = FormLogin()
    if request.method == 'POST':
        #conexion a la base de datos para iniciar sesion
        user = escape(form.correo.data)
        passw = escape(form.contrasena.data)
        userRequest = None
        passwordRequest = None

        try:
            with sqlite3.connect("HRC.db") as con:
                cur = con.cursor()
                consulta = cur.execute("SELECT email, password, rol, cedula FROM usuarios WHERE email=? and password = ?", [user, passw]).fetchone()
                print(consulta)
                con.commit()
                if consulta != None:
                    userRequest = consulta[0]
                    passwordRequest = consulta[1]
                    rol = consulta[2]  
                    userId = consulta[3]
        except Error: 
            flash('Error al conectar con la base de datos')

        if (user == userRequest and passw == passwordRequest):
            session['rol'] = rol
            session['user'] = userRequest
            session['cedula'] = userId
            return redirect(url_for("home"))
        else:
            if(user != userRequest):
                flash('Usuario incorrecto')
            elif(passw != passwordRequest):
                flash('Verifique la contraseña e intente nuevamente')
            return render_template('login.html',form=form)
    else:
        return render_template('login.html',form=form)  

@app.route('/logout')
def logout():
    if "rol" in session:
        session.pop("rol", None)
        return redirect(url_for("login"))
    else:
        return redirect(url_for("login"))
    

@app.route('/registro', methods=['GET', 'POST'])
def registro():
    form=FormRegistro()
    try:
        if request.method == 'POST':
            primerNombre = escape(form.Primer_nombre.data)
            segudoNombre = escape(form.Segundo_nombre.data)
            primerApellido = escape(form.Primer_apellido.data)
            segudoApellido = escape(form.Segundo_apellido.data)
            cedula = escape(form.identificacion.data)
            correo = escape(form.correo.data)
            passw = escape(form.contrasena.data)
            passwVerificacion = escape(form.confirmacion_contrasena.data)
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
                        yag = yagmail.SMTP("pruebasluismintic", "Darkluise2")
                        yag.send(to=correo, subject="Activa tu cuenta",contents="Bienvenido, usa este link para activar tu cuenta")
                        flash("Hola {} {} Revisa tu correo para activar tu cuenta".format(primerNombre,primerApellido))
                        return redirect(url_for("login"))
                except Error:
                        flash("Error al guardar el usuario, por favor intente de nuevo.")
                        return render_template('registro.html',form=form)
        else:
            return render_template('registro.html',form=form)
    except:
        return render_template('registro.html',form=form)

@app.route('/login/recuperacion', methods=['GET', 'POST'])
def recuperacion():
    if request.method == 'POST':
        correo = escape(request.form['correo'])
        error=None

        if not utils.isEmailValid(correo):
            error = "Correo invalido."
            flash(error)
            return render_template("recuperacion.html")
        
        try:
            with sqlite3.connect("HRC.db") as con:
                cur = con.cursor()
                consulta = cur.execute("SELECT pNombre,pApellido,email FROM usuarios WHERE email=?", [correo]).fetchone()
                print(consulta)
                con.commit()
                if consulta!=None:
                    return redirect(url_for("mensaje"))       
                else:
                    error = "Correo no existe en la base de datos"
                    flash(error)
                    return render_template('recuperacion.html')
        except Error: 
            flash('Error al conectar con la base de datos')

    else:
        return render_template('recuperacion.html')


@app.route('/login/recuperacion/mensaje', methods=['GET', 'POST'])
def mensaje():
    return render_template('mensaje.html')

#--------------------------------------------------------------JOSE------------------------------------------------------------------------
@app.route("/habitaciones", methods=['GET', 'POST'])
def home():
    if "rol" in session:
        rol=session["rol"]

        if request.method == 'GET':
            form = formHabitaciones()
            try:
                with sqlite3.connect("D:\database\HRC.db") as con:
                    con.row_factory = sqlite3.Row 
                    cur = con.cursor()
                    cur.execute("SELECT * FROM habitacion")
                    row = cur.fetchone()
                    if row is None:
                        flash("Habitacion no existente")
                    return render_template("habitaciones.html",form=form,row=row,rol=rol)
            except Error:
                #con.rollback()
                print(Error)
                return "Error en el método"
        elif request.method == 'POST':
            form = formHabitaciones()
            try:
                with sqlite3.connect("D:\database\HRC.db") as con:
                    con.row_factory = sqlite3.Row 
                    cur = con.cursor()
                    cur.execute("SELECT * FROM habitacion")
                    row = cur.fetchone()
                    if row is None:
                        flash("Habitacion no existente")
                    return render_template("habitaciones.html",form=form,row=row,rol=rol)
            except Error:
                #con.rollback()
                print(Error)
        else:
            return "Error en el método"
    else:
        flash("Accion no permita por favor inicie sesión")
        return render_template('error.html')    

@app.route("/habitaciones/get", methods=['GET', 'POST'])
def Habitaciones_get():
    if "rol" in session:
        rol=session["rol"]
        form = formHabitaciones()
        if request.method == 'POST':
            idHabitacion = form.idHabitacion.data
            try:
                with sqlite3.connect("D:\database\HRC.db") as con:
                    con.row_factory = sqlite3.Row
                    cur = con.cursor()
                    cur.execute("SELECT * FROM habitacion WHERE id = ?", [idHabitacion])
                    row = cur.fetchone()
                    if row is None:
                        flash("Habitacion no existente")
                    return render_template("habitacionesGet.html",form=form, row=row, rol=rol)
            except Error:
                #con.rollback()
                print(Error)
        return "Error en el método"
    else:
        flash("Accion no permita por favor inicie sesión")
        return render_template('error.html')

@app.route("/habitaciones/list", methods=["GET", "POST"])
def Habitaciones_list():
    if "rol" in session:
        rol=session["rol"]
        form = formHabitaciones()
        try:
            with sqlite3.connect("D:\database\HRC.db") as con:
                con.row_factory = sqlite3.Row 
                cur = con.cursor()
                cur.execute("SELECT * FROM habitacion")
                row = cur.fetchall()
                return render_template("habitacionesList.html",form=form, row=row, rol = rol)
        except  Error:
            #con.rollback()
            print(Error)
    else:
        flash("Accion no permita por favor inicie sesión")
        return render_template('error.html')

@app.route("/habitaciones/disp", methods=['GET', 'POST'])
def Habitaciones_disp():
    if "rol" in session:
        form = formHabitaciones()
        if request.method == 'POST':
            estado = form.estado.data
            if estado:
                estado = 1
            else:
                estado = 0
            try:
                with sqlite3.connect("D:\database\HRC.db") as con:
                    con.row_factory = sqlite3.Row 
                    cur = con.cursor()
                    cur.execute("SELECT * FROM habitacion WHERE  disponibilidad = ?", [estado])
                    row = cur.fetchall()
                    if row is None:
                        flash("No hay habitaciones disponibles")
                    return render_template("habitacionesList.html",form=form, row=row, rol=session['rol'])
            except Error:
                #con.rollback()
                print(Error)
        return "Error en el método"
    else:
        flash("Accion no permita por favor inicie sesión")
        return render_template('error.html')

#---------------------------------------------------------------------------ADRI-----------------------------------
@app.route('/habitaciones', methods=['GET', 'POST'])
def pagina_admin():
    if "rol" in session:
        return render_template('habitaciones.html', rol=session['rol'])
    else:
        flash("Accion no permita por favor inicie sesión")
        return render_template('error.html')

@app.route('/habitaciones/panelAdm', methods=['GET'])
def panelAdm():
    if "rol" in session:
        return render_template("panel_adm.html",rol=session['rol'])
    else:   
        flash("Accion no permita por favor inicie sesión")
        return render_template('error.html')

@app.route('/habitaciones/gestionHab', methods=['GET', 'POST']) 
def gestionHab():
    
    if 'rol' in session:
        if request.method == 'POST':
            nombreHab = request.form['name_habE']
            idHab = request.form['id_habE']
            descripcion = request.form['descripcionE']
            capacidad = request.form['capacidadE']
            camas = request.form['numero_camasE']
            valor = request.form['precioE']
            try:
                with sqlite3.connect('D:\database\HRC.db') as con:
                    cur = con.cursor()
                    cur.execute(f'UPDATE habitacion(nombre, descripcion, disponibilidad, cantCamas, capMax, precio) SET nombre ="{nombreHab}",  descripcion ="{descripcion}" , cantCamas = {camas}, capMax = {capacidad}, precio = {valor} WHERE id = ?', (idHab))
                    con.commit()
            except Error:
                return('<p>Error al realizar la operacion</p>')
        return render_template('editarHab.html')
    else:
        flash('Accion no permita por favor inicie sesión')
        return render_template('error.html')

@app.route('/habitaciones/panelAdm/gestionHab/agregarH', methods=['GET', 'POST'])
def agregarH():
    if "rol" in session:
        if request.method == 'POST':
            nombreHab = request.form['name_hab_add']
            idHab = request.form['id_hab_add']
            descripcion = request.form['descripcion_add']
            disponibilidad = 1
            numCam = request.form['numero_camas_add']
            capacidad= request.form['capacidad_add']
            valor = request.form['valor_add']
            try:
                with sqlite3.connect('D:\database\HRC.db') as con:
                    cur = con.cursor()
                    cur.execute('INSERT INTO habitacion(id, nombre, descripcion, disponibilidad, cantCamas, capMax, precio) VALUES (?,?,?,?,?,?,?)', (idHab, nombreHab, descripcion, disponibilidad, numCam, capacidad, valor))
                    con.commit()
                    return render_template("agregaHab.html", rol = session['rol'])
            except sqlite3.Error:
                print (sqlite3.Error)
                return('<p>Error al realizar la operacion</p>')
        return render_template("agregaHab.html", rol = session['rol'])
    else:
        flash("Accion no permita por favor inicie sesión")
        return render_template('error.html')

@app.route('/habitaciones/panelAdm/gestionHab/editarH', methods=['GET', 'POST']) 
def editarH():
    if "rol" in session:
        return render_template("editarHab.html", rol=session['rol'])
    else:
        flash("Accion no permita por favor inicie sesión")
        return render_template('error.html')

@app.route('/habitaciones/panelAdm/gestionHab/eliminarH', methods=['GET'])
def eliminarH():
    if "rol" in session:
        return render_template("eliminar.html",rol=session['rol'])
    else:
        flash("Accion no permita por favor inicie sesión")
        return render_template('error.html')

#------------------------------------------------JULIAN----------------------------------------------------------
@app.route('/reserva/<idHab>', methods=['GET'])
def load_reserva(idHab = None):
    
    if "rol" in session:
        try:
            with sqlite3.connect("D:\database\HRC.db") as con:
                con.row_factory = sqlite3.Row 
                cur = con.cursor()
                cur.execute("SELECT * FROM habitacion WHERE id = ?", [idHab])
                row= cur.fetchone()
                con.commit()
                if row is None:
                    flash("No hay habitaciones disponibles")
                return render_template('reserva.html', idHab = idHab, row = row)
        except Error:
            return 'Error al conectar la base de datos'
    else:
        flash("Accion no permita por favor inicie sesión")
        return render_template('error.html')

@app.route('/reserva/mensaje_reserva', methods=["GET", "POST"])
def reserva():
    if "rol" in session:
        if request.method == 'POST':
            checkin = request.form['checkin']
            checkout = request.form['checkout']
            correo = request.form['emailR']
            telefono = request.form['numeroR']
            preferencia = request.form['preferenciasR']
            check = request.form['typePay']
            idHab = request.form['habitacion']
            cedula = session['cedula']
            cardName = request.form['name-card']
            cardNum = request.form['number-card']
            cvc = request.form['cvc']
            caducidad = request.form['caducidad']
            print(cedula)


            if utils.isEmailValid(correo):
                if checkin == checkout:
                    flash('Las fechas de entrada y salida no pueden ser iguales')
                    return render_template('reserva.html')
                try:
                    with sqlite3.connect('D:\database\HRC.db') as con:
                        cur = con.cursor()
                        cur.execute('ISERT INTO reserva(checkin, checkout, email, telefono, preferencia, fPago, idHabitacion, cedula) VALUES(?,?,?,?,?,?,?,?)', (checkin, checkout, correo, telefono, preferencia, check, idHab, cedula))
                        con.commit()
                except Error:
                    return "<h1>Error al realizar la conexion</h1>"
                return "<p>Reserva realizada con exito</p>"
            else:
                return "<h1>Error al realizar la reserva</h1>"
    else:
        flash("Accion no permita por favor inicie sesión")
        return render_template('error.html')

#-----------------------------------------------------------------------------------JESUS--------------------------------------------------------
@app.route("/misHabitaciones")
def mishabitaciones():
    if "rol" in session:
        return render_template("gestion_comentarios.html")
    else:
        flash("Accion no permita por favor inicie sesión")
        return render_template('error.html')

if __name__ == '__main__':
    app.run(debug=True, port=8000)