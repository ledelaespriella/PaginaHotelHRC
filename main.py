from sqlite3.dbapi2 import Error
from formularios import FormLogin,FormRegistro,formCambio_password,formHabitaciones,formHab
import os
import utils
from flask import Flask, request, flash, session
from flask import render_template
from flask.helpers import url_for
from werkzeug.utils import redirect
from markupsafe import escape
#import yagmail
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
            #print(session)
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
        else:
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
                flash('Error al conectar con la base de datos')
                return render_template('recuperacion.html')
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
            
            if not utils.isPasswordValid(nuevoPassword):
                error = "Contraseña invalida por favor registre una correcta."
                flash(error)
                return render_template("recuperacionPassw.html",form=form)
            
            if nuevoPassword==confirmacionPassword:
                try:
                    with sqlite3.connect("HRC.db") as con:
                        cur = con.cursor()
                        consulta = cur.execute("UPDATE usuarios SET password=? WHERE email=?",[nuevoPassword,usuario])
                        con.commit()
                        if consulta!=None:
                            return render_template('mensaje.html')        
                        else:
                            error = "Error en la consulta a la base de datos"
                            flash(error)
                            return render_template('recuperacionPassw.html',form=form)
                except Error: 
                    flash('Error al conectar con la base de datos')
                    print (Error)
                    return render_template('recuperacionPassw.html',form=form)
            else:
                error = "Contraseñas no coinciden. Por favor verifique e intente de nuevo"
                flash(error)
                return render_template('recuperacionPassw.html',form=form)
        else:
            return render_template('recuperacionPassw.html',form=form)
    else:
        flash("Accion no permita por favor inicie sesión")
        return render_template('error.html') 

@app.errorhandler(404)
def page_not_found(error):
	return render_template("errores.html",error="404 Pagina no encontrada",mensaje="Lo sentimos, se ha producido un error, no se ha encontrado la página solicitada."), 404

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


@app.errorhandler(404)
def page_not_found(error):
	return render_template("errores.html",error="404 Pagina no encontrada",mensaje="Lo sentimos, se ha producido un error, no se ha encontrado la página solicitada."), 404


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
                    if row is None:
                        flash("Habitacion no existente")
                    return render_template("habitacionesGet.html",form=form, row=row)
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
        form = formHabitaciones()
        try:
            with sqlite3.connect("HRC.db") as con:
                con.row_factory = sqlite3.Row 
                cur = con.cursor()
                cur.execute("SELECT * FROM habitacion")
                row = cur.fetchall()
                return render_template("habitacionesList.html",form=form, row=row)
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
        rol=session["rol"]
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
                    return render_template("habitaciones.html",form=form, row=row,rol=rol)
            except Error:
                #con.rollback()
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
                    return render_template("habitaciones.html",form=form, row=row,rol=rol)
            except Error:
                #con.rollback()
                print(Error)
        else:
            return "Error en el método"
    else:
        flash("Accion no permita por favor inicie sesión")
        return render_template('error.html')

@app.route('/habitaciones/panelAdm', methods=['GET'])
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
        form = formHab()
        return render_template("editarHab.html", form=form)
    else:
        flash("Accion no permita por favor inicie sesión")
        return render_template('error.html')    

@app.route('/admin/panelAdm/gestionHab/agregarH', methods=['POST'])
def nuevaH():
    if "rol" in session:
        form = formHab()
        if request.method == 'POST':
            idHabitacion = form.idHab.data
            nombre = form.nomHab.data
            capM = form.capMax.data
            precio = form.precio.data
            numC = form.numCama.data
            desc = form.descrip.data
            try:
                with sqlite3.connect("HRC.db") as con:
                    cur = con.cursor() #Manipula la conexión a la BD
                    cur.execute("INSERT INTO habitacion(id, nombre, descripcion, disponibilidad, cantCamas, capMax, precio, calificacion) VALUES (?,?,?,True,?,?,?,0)", (idHabitacion, nombre, desc, numC, capM, precio) )
                    con.commit() #Confirmar la transacción
                    return render_template("save.html",error="Felicidades",mensaje="La información se ha guardado satisfactoriamente en la base de datos")                    
            except Error:
                return render_template("errores.html",error="500 Error en el servidor",mensaje="Lo sentimos, se ha producido un error en el servidor. Estaremos solucionando a la mayor brevedad el inconveniente.")
        return render_template("save.html",error="Error",mensaje="No se pudo guardar la información")
    else:
        flash("Accion no permita por favor inicie sesión")
        return render_template('error.html')

@app.route("/admin/panelAdm/gestionHab/lista", methods=["GET", "POST"])
def listH():
    if "rol" in session:
        try:
            with sqlite3.connect("HRC.db") as con:
                con.row_factory = sqlite3.Row #Convierte la respuesta de la BD en un diccionario
                cur = con.cursor()
                cur.execute("SELECT id, nombre, cantCamas, capMax, precio, disponibilidad FROM habitacion ORDER BY id")
                row = cur.fetchall()
                return render_template("listaHab.html", row=row)
        except  Error:
            return render_template("errores.html",error="500 Error en el servidor",mensaje="Lo sentimos, se ha producido un error en el servidor. Estaremos solucionando a la mayor brevedad el inconveniente.")
    else:
        flash("Accion no permita por favor inicie sesión")
        return render_template('error.html')


@app.route("/admin/panelAdm/gestionHab/get", methods=['GET', 'POST'])
def buscaH():
    if "rol" in session:
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
                        flash("Habitación no encontrada en la BD")
                    return render_template("agregaHab.html", row=row) 
            except Error:
                return render_template("errores.html",error="500 Error en el servidor",mensaje="Lo sentimos, se ha producido un error en el servidor. Estaremos solucionando a la mayor brevedad el inconveniente.")
        return "Error en el método"
    else:
        flash("Accion no permita por favor inicie sesión")
        return render_template('error.html')


@app.route('/admin/panelAdm/gestionHab/editarH', methods=['POST']) 
def editarH():
    if "rol" in session:
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
                        return render_template("save.html",error="Bien Hecho",mensaje="Habitación modificada correctamente.")
                    else:
                        return render_template("save.html",error="Error",mensaje=" No fue posible modificar la habitación.") 
            except Error:
                return render_template("errores.html",error="500 Error en el servidor",mensaje="Lo sentimos, se ha producido un error en el servidor. Estaremos solucionando a la mayor brevedad el inconveniente.")
    else:
        flash("Accion no permita por favor inicie sesión")
        return render_template('error.html')

@app.route('/admin/panelAdm/gestionHab/eliminarH',  methods=['GET', 'POST'])
def eliminarH():
    if "rol" in session:
        form=formHab()
        idHabitacion = form.idHab.data
        try:
            with sqlite3.connect("HRC.db") as con:
                cur = con.cursor()
                cur.execute("DELETE FROM habitacion WHERE id=?", [idHabitacion] )
                if con.total_changes > 0:
                    return render_template("save.html",error="¡Hecho!",mensaje="La habitación ha sido eliminada correctamente.")
                else:
                    return render_template("save.html",error="Error",mensaje="Es posible que la habitación no exista.")
        except Error:
            return render_template("errores.html",error="500 Error en el servidor",mensaje="Lo sentimos, se ha producido un error en el servidor. Estaremos solucionando a la mayor brevedad el inconveniente.")
    else:
        flash("Accion no permita por favor inicie sesión")
        return render_template('error.html')

#julian
@app.route('/reserva/<idHab>')
def load_reserva(idHab):
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
                    with sqlite3.connect('HRC.db') as con:
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