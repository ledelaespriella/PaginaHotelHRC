from sqlite3.dbapi2 import Error
from formularios import FormLogin,FormRegistro, formCambio_password, formHabitaciones,formHab
import os
import utils
from flask import Flask, request, flash, session
from flask import render_template
from flask.helpers import url_for
from werkzeug.utils import redirect
from markupsafe import escape
import yagmail
import sqlite3
import hashlib
from werkzeug.security import generate_password_hash as Gph
from werkzeug.security import check_password_hash as Cph
from datetime import datetime #para obtener la fecha actual
import json

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
        #passwordRequest = None
        
        try:
            with sqlite3.connect("HRC.db") as con:
                cur = con.cursor()
                consulta = cur.execute("SELECT email, password, rol, cedula FROM usuarios WHERE email=?", [user]).fetchone()
                print(consulta)
                con.commit()
                
                if consulta!=None:
                    userRequest = consulta[0]
                    hashPass=consulta[1]
                    rol = consulta[2]  
                    userId = consulta[3]
        except Error:
            return render_template("errores.html",error="500 Error en el servidor",mensaje="Lo sentimos, se ha producido un error en el servidor. Estaremos solucionando a la mayor brevedad el inconveniente.") 
            #flash('Error al conectar con la base de datos')

        if (user == userRequest and Cph(hashPass,passw)):
            session['rol'] = rol
            session['user']= userRequest
            session['cedula']=userId
            if(rol == 'final'):
                print(session['rol'])
                return redirect(url_for("home"))
            elif(rol == 'admin'):
                return redirect(url_for("panelAdm"))
            elif(rol == 'supAdmin'):
                return redirect(url_for("panelAdm"))
        else:
            if(user != userRequest):
                flash('Usuario incorrecto')
            elif not(Cph(hashPass,passw)):
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
                HashPass=Gph(passw)
                try:
                    with sqlite3.connect('HRC.db') as con:
                        cur = con.cursor()
                        cur.execute('INSERT INTO usuarios(cedula, pNombre, sNombre, pApellido, sApellido, email, password, rol) VALUES (?,?,?,?,?,?,?,?)', (cedula, primerNombre, segudoNombre, primerApellido, segudoApellido, correo, HashPass, rol))
                        con.commit()
                        yag = yagmail.SMTP("pruebasluismintic", "Darkluise2")
                        yag.send(to=correo, subject="Activa tu cuenta",contents="Bienvenido, usa este link para ingresar sesion:\n")
                        flash("Hola {} {} Revisa tu correo para verificar la creación del usuario".format(primerNombre,primerApellido))
                        return redirect(url_for("login"))
                except Error:
                    flash("Error al guardar el usuario, por favor intente de nuevo.")
                    return render_template("errores.html",error="500 Error en el servidor",mensaje="Lo sentimos, se ha producido un error en el servidor. Estaremos solucionando a la mayor brevedad el inconveniente.") 
        else:
            return render_template('registro.html',form=form)
    except:
        return render_template('registro.html',form=form)

@app.route('/login/recuperacion', methods=['GET', 'POST'])
def recuperacion():
    if request.method == 'POST':
        correo = escape(request.form['correo'])
        error=None

        if utils.isEmailValid(correo):
            try:
                with sqlite3.connect("HRC.db") as con:
                    cur = con.cursor()
                    consulta = cur.execute("SELECT pNombre,pApellido,email FROM usuarios WHERE email=?", [correo]).fetchone()
                    print(consulta)
                    con.commit()
                    if consulta!=None:
                        usuario=consulta[2]
                        session['user']=usuario
                        return redirect(url_for("mensaje"))       
                    else:
                        error = "Correo no existe en la base de datos, por favor registrarse."
                        flash(error)
                        return redirect(url_for("registro"))
            except Error: 
                return render_template("errores.html",error="500 Error en el servidor",mensaje="Lo sentimos, se ha producido un error en el servidor. Estaremos solucionando a la mayor brevedad el inconveniente.") 
        else:
            error = "Correo invalido."
            flash(error)
            return render_template("recuperacion.html")         
    else:
        return render_template('recuperacion.html')


@app.route('/login/recuperacion/mensaje', methods=['GET', 'POST'])
def mensaje():
    if 'user' in session:
        usuario = session['user']
        form = formCambio_password()
        if request.method == 'POST':
            nuevoPassword = escape(form.contrasenaNueva.data)
            confirmacionPassword = escape(form.confirmacion_contrasena.data)
            
            if utils.isPasswordValid(nuevoPassword):    
                if nuevoPassword==confirmacionPassword:
                    HashPass=Gph(nuevoPassword)
                    try:
                        with sqlite3.connect("HRC.db") as con:
                            cur = con.cursor()
                            consulta = cur.execute("UPDATE usuarios SET password=? WHERE email=?",[HashPass,usuario])
                            con.commit()
                            if consulta!=None:
                                return render_template('mensaje.html')        
                            else:
                                error = "Error en la consulta a la base de datos"
                                flash(error)
                                return render_template('recuperacionPassw.html',form=form)
                    except Error: 
                        return render_template("errores.html",error="500 Error en el servidor",mensaje="Lo sentimos, se ha producido un error en el servidor. Estaremos solucionando a la mayor brevedad el inconveniente.") 
                else:
                    error = "Contraseñas no coinciden. Por favor verifique e intente de nuevo"
                    flash(error)
                    return render_template('recuperacionPassw.html',form=form)
            else:
                error = "Contraseña invalida por favor registre una correcta."
                flash(error)
                return render_template("recuperacionPassw.html",form=form)  
        else:
            return render_template('recuperacionPassw.html',form=form)
    else:
        flash("Accion no permita por favor inicie sesión")
        return render_template('error.html') 

@app.errorhandler(404)
def page_not_found(error):
    if "rol" in session:
        session.pop("rol", None)
        return render_template("errores.html",error="404 Pagina no encontrada",mensaje="Lo sentimos, se ha producido un error, no se ha encontrado la página solicitada."), 404
    else:
        return render_template("errores.html",error="404 Pagina no encontrada",mensaje="Lo sentimos, se ha producido un error, no se ha encontrado la página solicitada."), 404

@app.errorhandler(500)
def internal_server_error(error):
    if "rol" in session:
        session.pop("rol", None)
        return render_template("errores.html",error="500 Error en el servidor",mensaje="Lo sentimos, se ha producido un error en el servidor. Estaremos solucionando a la mayor brevedad el inconveniente."), 500
    else:
        return render_template("errores.html",error="500 Error en el servidor",mensaje="Lo sentimos, se ha producido un error en el servidor. Estaremos solucionando a la mayor brevedad el inconveniente."), 500


#--------------------------------------------------------------JOSE------------------------------------------------------------------------
@app.route("/habitaciones", methods=['GET', 'POST'])
def home():
    if "rol" in session:
        rol=session["rol"]

        if request.method == 'GET':
            form = formHabitaciones()
            try:
                with sqlite3.connect("HRC.db") as con:
                    con.row_factory = sqlite3.Row 
                    cur = con.cursor()
                    cur.execute("SELECT * FROM habitacion")
                    row = cur.fetchone()
                    hab = row['id']
                    rowC = cur.execute('SELECT * FROM comentario WHERE idHabitacion = ?', [hab]).fetchall()
                    con.commit()
                    if row is None:
                        flash("Habitacion no existente")
                    return render_template("habitaciones.html", form=form, row=row, rol=rol, cant = len(rowC))
            except Error:
                return render_template("errores.html",error="500 Error en el servidor",mensaje="Lo sentimos, se ha producido un error en el servidor. Estaremos solucionando a la mayor brevedad el inconveniente.") 
        elif request.method == 'POST':
            form = formHabitaciones()
            try:
                with sqlite3.connect("HRC.db") as con:
                    con.row_factory = sqlite3.Row 
                    cur = con.cursor()
                    cur.execute("SELECT * FROM habitacion")
                    row = cur.fetchone()
                    hab = row['id']
                    rowC = cur.execute('SELECT * FROM comentario WHERE idHabitacion = ?', [hab]).fetchall()
                    con.commit()
                    if row is None:
                        flash("Habitacion no existente")
                    return render_template("habitaciones.html", form=form, row=row, rol=rol, cant = len(rowC))
            except Error:
                return render_template("errores.html",error="500 Error en el servidor",mensaje="Lo sentimos, se ha producido un error en el servidor. Estaremos solucionando a la mayor brevedad el inconveniente.") 
        else:
            return render_template("errores.html",error="Error en el metodo",mensaje="Lo sentimos, se ha producido un error. Estaremos solucionando a la mayor brevedad el inconveniente.") 
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
                with sqlite3.connect("HRC.db") as con:
                    con.row_factory = sqlite3.Row
                    cur = con.cursor()
                    cur.execute("SELECT * FROM habitacion WHERE id = ?", [idHabitacion])
                    row = cur.fetchone()
                    hab = row['id']
                    rowC = cur.execute('SELECT * FROM comentario WHERE idHabitacion = ?', [hab]).fetchall()
                    con.commit()
                    if row is None:
                        flash("Habitacion no existente")
                    return render_template("habitaciones.html", form=form, row=row, rol=rol, cant = len(rowC))
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
            with sqlite3.connect("HRC.db") as con:
                con.row_factory = sqlite3.Row 
                cur = con.cursor()
                cur.execute("SELECT * FROM habitacion")
                row = cur.fetchall()
                con.commit()
                rowC = {}
                for r in row:
                    print(len(rowC))
                    c = cur.execute('SELECT * FROM comentario WHERE idHabitacion = ?', [r['id']]).fetchall()
                    cont = len(c)
                    print(cont)
                    rowC.update({r['id']: cont})
                    con.commit()
                   
                return render_template("habitacionesList.html", form=form, row=row, rol = rol, rowC = rowC)
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
                with sqlite3.connect("HRC.db") as con:
                    con.row_factory = sqlite3.Row 
                    cur = con.cursor()
                    cur.execute("SELECT * FROM habitacion WHERE  disponibilidad = ?", [estado])
                    row = cur.fetchall()
                    con.commit()
                    rowC = {}
                for r in row:
                    print(len(rowC))
                    c = cur.execute('SELECT * FROM comentario WHERE idHabitacion = ?', [r['id']]).fetchall()
                    cont = len(c)
                    print(cont)
                    rowC.update({r['id']: cont})
                    con.commit()
                return render_template("habitacionesList.html", form=form, row=row, rol = session['rol'], rowC = rowC)
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
        rol=session["rol"]
        if request.method == 'GET':
            form = formHabitaciones()
            try:
                with sqlite3.connect("HRC.db") as con:
                    con.row_factory = sqlite3.Row 
                    cur = con.cursor()
                    cur.execute("SELECT * FROM habitacion")
                    row = cur.fetchone()
                    con.commit()
                    if row is None:
                        flash("Habitacion no existente")
                    return render_template("habitaciones.html",form=form, row=row, rol=rol)
            except Error:
                return render_template("errores.html",error="500 Error en el servidor",mensaje="Lo sentimos, se ha producido un error en el servidor. Estaremos solucionando a la mayor brevedad el inconveniente.") 
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
                    return render_template("habitaciones.html",form=form, row=row,rol=rol)
            except Error:
                return render_template("errores.html",error="500 Error en el servidor",mensaje="Lo sentimos, se ha producido un error en el servidor. Estaremos solucionando a la mayor brevedad el inconveniente.") 
        else:
            return "Error en el método"
    else:
        flash("Accion no permita por favor inicie sesión")
        return render_template('error.html')

@app.route('/admin/panelAdm', methods=['GET'])
def panelAdm():
    if "rol" in session:
        rol = session["rol"]
        return render_template("panel_adm.html", rol=rol)
    else:
        flash("Accion no permita por favor inicie sesión")
        return render_template('error.html')

@app.route('/admin/panelAdm/gestionHab', methods=['GET', 'POST'])
def gestHab():
    if "rol" in session:
        rol = session["rol"]
        form = formHab()
        return render_template("editarHab.html", form=form,rol=rol)
    else:
        flash("Accion no permita por favor inicie sesión")
        return render_template('error.html')    

@app.route('/admin/panelAdm/gestionHab/agregarH', methods=['POST'])
def nuevaH():
    if "rol" in session:
        rol = session["rol"]
        form = formHab()
        if request.method == 'POST':
            idHabitacion = form.idHab.data
            nombre = form.nomHab.data
            capM = form.capMax.data
            precio = form.precio.data
            numC = form.numCama.data
            desc = form.descrip.data
            if idHabitacion=="" and nombre=="" and desc=="":
                return render_template("save.html",error="Error",mensaje="No se pudo guardar la información",rol=rol)
            else:
                try:
                    with sqlite3.connect("HRC.db") as con:
                        cur = con.cursor() #Manipula la conexión a la BD
                        cur.execute("INSERT INTO habitacion(id, nombre, descripcion, disponibilidad, cantCamas, capMax, precio, calificacion) VALUES (?,?,?,True,?,?,?,0)", (idHabitacion, nombre, desc, numC, capM, precio) )
                        con.commit() #Confirmar la transacción
                        return render_template("save.html",error="Felicidades",mensaje="La información se ha guardado satisfactoriamente en la base de datos",rol=rol)                    
                except Error:
                    return render_template("errores.html",error="500 Error en el servidor",mensaje="Lo sentimos, se ha producido un error en el servidor. Estaremos solucionando a la mayor brevedad el inconveniente.")
        return render_template("save.html",error="Error",mensaje="No se pudo guardar la información",rol=rol)
    else:
        flash("Accion no permita por favor inicie sesión")
        return render_template('error.html')

@app.route("/admin/panelAdm/gestionHab/lista", methods=["GET", "POST"])
def listH():
    if "rol" in session:
        rol = session["rol"]
        try:
            with sqlite3.connect("HRC.db") as con:
                con.row_factory = sqlite3.Row #Convierte la respuesta de la BD en un diccionario
                cur = con.cursor()
                cur.execute("SELECT id, nombre, cantCamas, capMax, precio, disponibilidad FROM habitacion ORDER BY id")
                row = cur.fetchall()
                return render_template("listaHab.html", row=row,rol=rol)
        except  Error:
            return render_template("errores.html",error="500 Error en el servidor",mensaje="Lo sentimos, se ha producido un error en el servidor. Estaremos solucionando a la mayor brevedad el inconveniente.")
    else:
        flash("Accion no permita por favor inicie sesión")
        return render_template('error.html')


@app.route("/admin/panelAdm/gestionHab/get", methods=['GET', 'POST'])
def buscaH():
    if "rol" in session:
        rol = session["rol"]
        form = formHab()
        if request.method == 'POST':
            idHabitacion = form.idHab.data
            try:
                with sqlite3.connect("HRC.db") as con:
                    con.row_factory = sqlite3.Row #Convierte la respuesta de la BD en un diccionario
                    cur = con.cursor()
                    cur.execute("SELECT id, nombre, descripcion, cantCamas, capMax, precio, disponibilidad FROM habitacion WHERE id = ?", [idHabitacion])
                    row = cur.fetchone()
                    if row is None:
                        return render_template("save.html",error="Error",mensaje="Es posible que la habitación no exista.",rol=rol)
                    else: 
                        return render_template("agregaHab.html", row=row,rol=rol) 
            except Error:
                return render_template("errores.html",error="500 Error en el servidor",mensaje="Lo sentimos, se ha producido un error en el servidor. Estaremos solucionando a la mayor brevedad el inconveniente.")
        else:
            return render_template("errores.html",error="500 Error en el servidor",mensaje="Lo sentimos, se ha producido un error en el servidor. Estaremos solucionando a la mayor brevedad el inconveniente.")
    else:
        flash("Accion no permita por favor inicie sesión")
        return render_template('error.html')


@app.route('/admin/panelAdm/gestionHab/editarH', methods=['POST']) 
def editarH():
    if "rol" in session:
        rol = session["rol"]
        form = formHab()
        if request.method == "POST":
            idHabitacion = form.idHab.data
            nombre = form.nomHab.data
            capM = form.capMax.data
            precio = form.precio.data
            numC = form.numCama.data
            desc = form.descrip.data
            dispo = form.disp.data
            try:
                with sqlite3.connect("HRC.db") as con:
                    cur = con.cursor() #Manipula la conexión a la BD
                    cur.execute("UPDATE habitacion SET nombre=?, descripcion=?, cantCamas=?, capMax=?, precio=?, disponibilidad=? WHERE id=?", [nombre, desc, numC, capM, precio, dispo, idHabitacion])
                    con.commit()
                    if con.total_changes > 0:
                        return render_template("save.html",error="Bien Hecho",mensaje="Habitación modificada correctamente.",rol=rol)
                    else:
                        return render_template("save.html",error="Error",mensaje=" No fue posible modificar la habitación.",rol=rol) 
            except Error:
                return render_template("errores.html",error="500 Error en el servidor",mensaje="Lo sentimos, se ha producido un error en el servidor. Estaremos solucionando a la mayor brevedad el inconveniente.")
    else:
        flash("Accion no permita por favor inicie sesión")
        return render_template('error.html')

@app.route('/admin/panelAdm/gestionHab/eliminarH',  methods=['GET', 'POST'])
def eliminarH():
    if "rol" in session:
        rol = session["rol"]
        form=formHab()
        idHabitacion = form.idHab.data
        try:
            with sqlite3.connect("HRC.db") as con:
                cur = con.cursor()
                cur.execute("DELETE FROM habitacion WHERE id=?", [idHabitacion] )
                if con.total_changes > 0:
                    return render_template("save.html",error="¡Hecho!",mensaje="La habitación ha sido eliminada correctamente.",rol=rol)
                else:
                    return render_template("save.html",error="Error",mensaje="Es posible que la habitación no exista.",rol=rol)
        except Error:
            return render_template("errores.html",error="500 Error en el servidor",mensaje="Lo sentimos, se ha producido un error en el servidor. Estaremos solucionando a la mayor brevedad el inconveniente.")
    else:
        flash("Accion no permita por favor inicie sesión")
        return render_template('error.html')


@app.route('/reservaAdmin/<idHab>')
def load_reservaAdmin(idHab = None):
    if "rol" in session:
        try:
            with sqlite3.connect("HRC.db") as con:
                con.row_factory = sqlite3.Row 
                cur = con.cursor()
                cur.execute("SELECT * FROM habitacion WHERE id = ?", [idHab])
                row= cur.fetchone()
                con.commit()
                if row is None:
                    flash("No hay habitaciones disponibles")
                return render_template('reservaAdmin.html', idHab = idHab, row = row)
        except Error:
            return render_template("errores.html",error="500 Error en el servidor",mensaje="Lo sentimos, se ha producido un error en el servidor. Estaremos solucionando a la mayor brevedad el inconveniente.") 
    else:
        flash("Accion no permita por favor inicie sesión")
        return render_template('error.html')

@app.route('/reserva/mensaje_reserva', methods=["GET", "POST"])
def reserva():
    if "rol" in session:
        if request.method == 'POST':
            if session['rol'] == 'final':
                checkin = request.form['checkin']
                checkout = request.form['checkout']
                correo = request.form['emailR']
                telefono = request.form['numeroR']
                preferencia = request.form['preferenciasR']
                check = request.form['typePay']
                idHab = int(request.form['habitacion'])
                cedula = session['cedula']
                
                cardName = request.form['name-card']
                cardNum = request.form['number-card']
                cvc = request.form['cvc']
                caducidad = request.form['caducidad']
                print(checkin, checkout, correo, telefono, preferencia, check,type(checkin), cedula)


                if utils.isEmailValid(correo):
                    if checkin == checkout:
                        flash('Las fechas de entrada y salida no pueden ser iguales')
                        return render_template('reserva.html')
                    try:
                        with sqlite3.connect('HRC.db') as con:
                            cur = con.cursor()
                            cur.execute('INSERT INTO reserva(checkin, checkout, email, telefono, preferencias, fPago, idHabitacion, cedula) VALUES(?,?,?,?,?,?,?,?)', (checkin, checkout, correo, telefono, preferencia, check, idHab, cedula))
                            con.commit()
                            cur.execute('UPDATE habitacion SET disponibilidad=? WHERE id=?', (0, idHab))
                            con.commit()
                            if check == 'tarjeta':
                                row = cur.execute('SELECT idReserva FROM reserva WHERE idHabitacion =? AND checkin = ?', [idHab, checkin]).fetchone()
                                con.commit()
                                cur.execute('INSERT INTO pagoTarjeta(numCard, nameCard, cvc, mmaa, idReserva) VALUES (?,?,?,?,?)', (cardNum, cardName, cvc, caducidad, row[0]))
                                con.commit()
                    except Error:
                        return render_template("errores.html",error="500 Error en el servidor",mensaje="Lo sentimos, se ha producido un error en el servidor. Estaremos solucionando a la mayor brevedad el inconveniente.") 
                    return render_template('reservaExitosa.html')
                else:
                    flash('Email  incorrecto')
                    return render_template('reserva.html')
            elif session['rol'] == 'supAdmin' or session['rol'] == 'Admin':
                checkin = request.form['checkin']
                checkout = request.form['checkout']
                correo = request.form['emailR']
                telefono = request.form['numeroR']
                preferencia = request.form['preferenciasR']
                check = request.form['typePay']
                idHab = int(request.form['habitacion'])
                cedula = int(request.form['cedulaR'])
                cardName = request.form['name-card']
                cardNum = request.form['number-card']
                cvc = request.form['cvc']
                caducidad = request.form['caducidad']

                if utils.isEmailValid(correo):
                    if checkin == checkout:
                        flash('Las fechas de entrada y salida no pueden ser iguales')
                        return render_template('reserva.html')
                    try:
                        with sqlite3.connect('HRC.db') as con:
                            cur = con.cursor()
                            cur.execute('INSERT INTO reserva(checkin, checkout, email, telefono, preferencias, fPago, idHabitacion, cedula) VALUES(?,?,?,?,?,?,?,?)', (checkin, checkout, correo, telefono, preferencia, check, idHab, cedula))
                            con.commit()
                            cur.execute('UPDATE habitacion SET disponibilidad=? WHERE id=?', (0, idHab))
                            con.commit()
                            if check == 'tarjeta':
                                row = cur.execute('SELECT idReserva FROM reserva WHERE idHabitacion =? AND checkin = ?', [idHab, checkin]).fetchone()
                                con.commit()
                                cur.execute('INSERT INTO pagoTarjeta(numCard, nameCard, cvc, mmaa, idReserva) VALUES (?,?,?,?,?)', (cardNum, cardName, cvc, caducidad, row[0]))
                                con.commit()
                        return render_template('reservaExitosa.html')
                    except Error:
                        return render_template("errores.html",error="500 Error en el servidor",mensaje="Lo sentimos, se ha producido un error en el servidor. Estaremos solucionando a la mayor brevedad el inconveniente.") 
                else:
                    flash('Email  incorrecto')
                    return render_template('reserva.html') 
    else:
        flash("Accion no permita por favor inicie sesión")
        return render_template('error.html')

@app.route('/habitaciones/comentarios/<idHab>', methods = ['GET', 'POST'])
def comentarios(idHab = None):

    if "rol" in session:
        form = formHabitaciones()
        try:
            with sqlite3.connect("HRC.db") as con:
                con.row_factory = sqlite3.Row
                cur = con.cursor() 
                cur.execute("SELECT * FROM habitacion WHERE id = ?", [idHab])
                row = cur.fetchone()
                rowC = cur.execute('SELECT * FROM comentario WHERE idHabitacion = ?', [idHab]).fetchall()
                con.commit()
                return render_template("comentarios.html",form=form, row=row, rowC = rowC, idHab = idHab)
        except  Error:
            return render_template("errores.html",error="500 Error en el servidor",mensaje="Lo sentimos, se ha producido un error en el servidor. Estaremos solucionando a la mayor brevedad el inconveniente.") 
    else:
        flash("Accion no permita por favor inicie sesión")
        return render_template('error.html')

@app.route('/habitaciones/disponible', methods = ['GET', 'POST'])
def disponible():
    if "rol" in session:
        return render_template('noDisponible.html')
    else:
        flash("Accion no permita por favor inicie sesión")
        return render_template('error.html')

#-----------------------------------------------------------------------------------JESUS--------------------------------------------------------
@app.route("/misHabitaciones", methods = ['GET', 'POST'])
def mishabitaciones():
    if 'rol' in session:
        _cedula = session['cedula']
        try:
            with sqlite3.connect("HRC.db") as con:
                con.row_factory = sqlite3.Row 
                cur = con.cursor()
                cur.execute("SELECT reserva.idHabitacion, reserva.checkout, comentario.comentario FROM reserva LEFT JOIN comentario ON comentario.idHabitacion = reserva.idHabitacion WHERE reserva.cedula = ?",[_cedula])
                row = cur.fetchall()
                return render_template("mishabitaciones.html", row=row)
        except  Error:
            return render_template("errores.html",error="500 Error en el servidor",mensaje="Lo sentimos, se ha producido un error en el servidor. Estaremos solucionando a la mayor brevedad el inconveniente.") 
    else:
        flash("Accion no permita por favor inicie sesión")
        return render_template('error.html')


@app.route("/misHabitaciones/save", methods=["POST"])
def guardar_comentario():
    if 'rol' in session:
        rol=session['rol']
        if request.method == 'POST':
        
            _comentario = request.form['comentario_hab']
            _fechaComentario = datetime.today().strftime('%Y/%m/%d')
            _idHabitacion = request.form['hab_a_comentar']
            _cedula = session['cedula']
            _calificacion=request.form['calificacion_hab']
            try:
                with sqlite3.connect('HRC.db') as con:
                    cur = con.cursor()
                    cur.execute('INSERT INTO comentario(comentario, fechaComentario, idHabitacion, cedula) VALUES (?,?,?,?)',(_comentario,_fechaComentario,_idHabitacion,_cedula))
                    con.commit() #Confirmar la transacción  
                    cur.execute('INSERT INTO calificacion(calificacion, idHabitacion, cedula) VALUES (?,?,?)',(_calificacion,_idHabitacion,_cedula))   
                    con.commit()
                    cur.execute("SELECT AVG(calificacion) FROM calificacion WHERE idHabitacion= ?",[_idHabitacion])
                    _vari=round(cur.fetchone()[0], 2)
                    cur.execute('UPDATE habitacion SET calificacion=? WHERE id=?',(_vari,_idHabitacion))   
                    flash('Comentario guardado exitosamente')
                    return redirect(url_for("mishabitaciones"))
                
            except Error:
                return render_template("errores.html",error="500 Error en el servidor",mensaje="Lo sentimos, se ha producido un error en el servidor. Estaremos solucionando a la mayor brevedad el inconveniente.") 
    else:
        flash("Accion no permita por favor inicie sesión")
        return render_template('error.html')
        
@app.route("/misHabitaciones/up", methods=["POST"])
def actualizar_comentario():
    if 'rol' in session:
        rol=session['rol']
        if request.method == 'POST':
            _comentario = request.form['comentario_hab']
            _fechaComentario = datetime.today().strftime('%Y/%m/%d')
            _idHabitacion = request.form['hab_a_comentar']
            _cedula = session['cedula']
            _calificacion=request.form['calificacion_hab']
            try:
                with sqlite3.connect('HRC.db') as con:
                    cur = con.cursor()
                    cur.execute('UPDATE comentario SET comentario =?, fechaComentario=? WHERE idHabitacion=? AND cedula=?',(_comentario,_fechaComentario,_idHabitacion,_cedula))
                    con.commit() 
                    cur.execute('UPDATE calificacion SET calificacion=? WHERE idHabitacion=? AND cedula=?',(_calificacion,_idHabitacion,_cedula))   
                    con.commit()
                    cur.execute("SELECT AVG(calificacion) FROM calificacion WHERE idHabitacion= ?",[_idHabitacion])
                    _vari=round(cur.fetchone()[0], 2)
                    cur.execute('UPDATE habitacion SET calificacion=? WHERE id=?',(_vari,_idHabitacion))   
                    flash('Comentario actualizado exitosamente')
                    return redirect(url_for("mishabitaciones"))
            except Error:
                return render_template("errores.html",error="500 Error en el servidor",mensaje="Lo sentimos, se ha producido un error en el servidor. Estaremos solucionando a la mayor brevedad el inconveniente.") 
    else:
        flash("Accion no permitida, por favor inicie sessión")
        return render_template('error.html')

@app.route("/misHabitaciones/delete", methods=["POST"])
def eliminar_comentario():
    if 'rol' in session:
        rol=session['rol']
        if request.method == 'POST':
            _idHabitacion = request.form['hab_a_comentar']
            _cedula = session['cedula']
          
            try:
                with sqlite3.connect('HRC.db') as con:
                    cur = con.cursor()
                    cur.execute('DELETE FROM comentario WHERE idHabitacion=? AND cedula=?',(_idHabitacion,_cedula))
                    con.commit() 
                    cur.execute('DELETE FROM calificacion WHERE idHabitacion=? AND cedula=?',(_idHabitacion,_cedula))   
                    con.commit()
                    cur.execute("SELECT AVG(calificacion) FROM calificacion WHERE idHabitacion= ?",[_idHabitacion])
                    if cur.fetchone():
                        _vari=0
                    else:
                        _vari=round(cur.fetchone()[0], 2)
                       
                    cur.execute('UPDATE habitacion SET calificacion=? WHERE id=?',(_vari,_idHabitacion))   
                    con.commit()
                    flash('Comentario eliminado exitosamente')
                    return redirect(url_for("mishabitaciones"))
            except Error:
                return render_template("errores.html",error="500 Error en el servidor",mensaje="Lo sentimos, se ha producido un error en el servidor. Estaremos solucionando a la mayor brevedad el inconveniente.") 
    else:
        flash("Accion no permitida, por favor inicie sessión")
        return render_template('error.html')

@app.route("/admin/panelAdm/gestion_usuarios", methods=['GET', 'POST'])
def gestionusuarios():
    if ('rol' in session) and session['rol']=="supAdmin":
        try:
            with sqlite3.connect("HRC.db") as con:
                con.row_factory = sqlite3.Row 
                cur = con.cursor()
                _correo="admin@gmail.com"
                cur.execute('SELECT * FROM usuarios WHERE email!=?',[_correo])
                row = cur.fetchall()
                return render_template("gestionUsuarios.html",row=row)
        except Error:
            return render_template("errores.html",error="500 Error en el servidor",mensaje="Lo sentimos, se ha producido un error en el servidor. Estaremos solucionando a la mayor brevedad el inconveniente.") 
    else:
        flash("Accion no permitida, por favor inicie sessión como adiministrador")
        return render_template('error.html')

@app.route("/admin/panelAdm/gestion_usuarios/delete", methods=["POST"])
def eliminar_usuarios():
    if ('rol' in session) and session['rol']=="supAdmin":
        _cedula_u=request.form['usuario_s']
        if request.method == 'POST':
            try:
                with sqlite3.connect('HRC.db') as con:
                    cur = con.cursor()
                    #Borrar actividad del usuario 
                    cur.execute('DELETE FROM comentario WHERE cedula=?',[_cedula_u])
                    con.commit()#borrar comentarios
                    cur.execute('DELETE FROM calificacion WHERE cedula=?',[_cedula_u])
                    con.commit()#borrar calificacion       
                    #Borrar Usuario
                    cur.execute('DELETE FROM usuarios WHERE cedula=?',[_cedula_u])
                    con.commit()
                    flash('Usuario eliminado exitosamente')
                    return redirect(url_for("gestionusuarios"))
            except Error:
                return render_template("errores.html",error="500 Error en el servidor",mensaje="Lo sentimos, se ha producido un error en el servidor. Estaremos solucionando a la mayor brevedad el inconveniente.") 
    else:
        flash("Accion no permitida, por favor inicie sessión como adiministrador")
        return render_template('error.html')

@app.route("/admin/panelAdm/gestion_usuarios/up", methods=["POST"])
def actualizar_usuarios():
    if ('rol' in session) and session['rol']=="supAdmin":
        _rol=request.form['rol_usuario']
        _cedula_u=request.form['usuario_s']
        if request.method == 'POST':
            try:
                with sqlite3.connect('HRC.db') as con:
                    cur = con.cursor()
                    cur.execute('UPDATE usuarios SET rol =? WHERE cedula=?',(_rol,_cedula_u))
                    con.commit() 
                    flash('Usuario actualizado exitosamente')
                    return redirect(url_for("gestionusuarios"))
            except Error:
                return render_template("errores.html",error="500 Error en el servidor",mensaje="Lo sentimos, se ha producido un error en el servidor. Estaremos solucionando a la mayor brevedad el inconveniente.")                 
    else:
        flash("Accion no permitida, por favor inicie sessión como adiministrador")
        return render_template('error.html')       


if __name__ == '__main__':
    app.run(debug=True, port=8000)