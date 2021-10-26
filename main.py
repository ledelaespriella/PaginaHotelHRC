from sqlite3.dbapi2 import Error
from formularios import FormLogin,FormRegistro,formHabitaciones,formHab
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

#luis
@app.route('/', methods=['GET'])
def inicio():
    return render_template('Home.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    form= FormLogin()
    if request.method == 'POST':
        user = escape(form.correo.data)
        passw = escape(form.contrasena.data)
        userRequest = None
        passwordRequest = None
        try:
            with sqlite3.connect("HRC.db") as con:
                cur = con.cursor()
                consulta = cur.execute("SELECT email, password, rol FROM usuarios WHERE email=? and password = ?", [user, passw]).fetchone()
                print(consulta)
                con.commit()
                if consulta!=None:
                    userRequest = consulta[0]
                    passwordRequest = consulta[1]
                    rol = consulta[2]       
        except Error: 
            flash('Error al conectar con la base de datos')
        if (user == userRequest and passw == passwordRequest):
            session['rol'] = rol
            #print(session)
            if(rol == 'final'):
                print(session['rol'])
                return redirect(url_for("home"))
            elif(rol == 'admin'):
                return redirect(url_for("home"))
            elif(rol == 'supAdmin'):
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
            print(rol)
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

#jose


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
                    return render_template("habitacionesList.html",form=form, row=row)
            except Error:
                #con.rollback()
                print(Error)
        return "Error en el método"
    else:
        flash("Accion no permita por favor inicie sesión")
        return render_template('error.html')

@app.route('/admin/habitaciones', methods=['GET', 'POST'])
def pagina_admin():
    if "rol" in session:
        admin="admin@gmail.com"
        return render_template('habitaciones.html',usuario=admin)
    else:
        flash("Accion no permita por favor inicie sesión")
        return render_template('error.html')

#rutas de adri

@app.route('/admin/panelAdm', methods=['GET'])
def panelAdm():
    if "rol" in session:
        admin="admin@gmail.com"
        return render_template("panel_adm.html",usuario=admin)
    else:
        flash("Accion no permita por favor inicie sesión")
        return render_template('error.html')

@app.route('/admin/panelAdm/gestionHab', methods=['GET', 'POST'])
def gestHab():
    form = formHab()
    return render_template("editarHab.html", form=form)


@app.route('/admin/panelAdm/gestionHab/agregarH', methods=['POST'])
def nuevaH():
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
                cur.execute("INSERT INTO habitacion(id, nombre, descripcion, cantCamas, capMax, precio) VALUES (?,?,?,?,?,?)", (idHabitacion, nombre, desc, numC, capM, precio) )
                con.commit() #Confirmar la transacción
                return "Guardado satisfactoriamente"
        except Error:
            con.rollback()
            print(Error)
    return "No se pudo guardar"

@app.route("/admin/panelAdm/gestionHab/get", methods=['GET', 'POST'])
def buscaH():
    form = formHab()
    if request.method == 'POST':
        idHabitacion = form.idHab.data
        try:
            with sqlite3.connect("HRC.db") as con:
                con.row_factory = sqlite3.Row #Convierte la respuesta de la BD en un diccionario
                cur = con.cursor()
                cur.execute("SELECT * FROM habitacion WHERE id = ?", [idHabitacion])
                row = cur.fetchone()
                if row is None:
                    flash("Estudiante no se encuentra en la BD")
                return render_template("agregaHab.html", row=row) ################ REVISAR #####################
        except Error:
            con.rollback()
            print(Error)
    return "Error en el método"


@app.route('/admin/panelAdm/gestionHab/editarH', methods=['POST']) 
def editarH():
    form = formHab()
    if request.method == "POST":
        idHabitacion = form.idHab.data
        nombre = form.nomHab.data
        capM = form.capMax.data
        precio = form.precio.data
        numC = form.numCama.data
        desc = form.descrip.data
        try:
            with sqlite3.connect("HRC.db") as con:
                cur = con.cursor() #Manipula la conexión a la BD
                cur.execute("UPDATE habitacion SET nombre=?, descripcion=?, cantCamas=?, capMax=?, precio=? WHERE id=?", [nombre, desc, numC, capM, precio, idHabitacion])
                con.commit()
                if con.total_changes > 0:
                    mensaje = " Habitación modificada exitosamente"
                else:
                    mensaje = " No fue posible modificar la habitación"
        except Error:
            con.rollback()
            print(Error)
        finally:
            return mensaje

@app.route('/admin/panelAdm/gestionHab/msjeliminarH',  methods=['GET', 'POST'])
def msjelimina():
    form = formHab()
    return render_template("eliminar.html", form=form)

@app.route('/admin/panelAdm/gestionHab/eliminarH',  methods=['GET', 'POST'])
def eliminarH():
    form=formHab()
    idHabitacion = form.idHab.data
    try:
        with sqlite3.connect("HRC.db") as con:
            cur = con.cursor()
            cur.execute("DELETE FROM habitacion WHERE id=?", [idHabitacion] )
            if con.total_changes > 0:
                mensaje = "Habitación eliminada con éxito"
            else:
                mensaje = "Es posible que la habitación no exista"
    except Error:
        con.rollback()
        print(Error)
    finally:
        return mensaje


#julian
@app.route('/reserva')
def load_reserva():
    if "rol" in session:
        return render_template('reserva.html')
    else:
        flash("Accion no permita por favor inicie sesión")
        return render_template('error.html')

@app.route('/reserva/mensaje_reserva', methods=["GET", "POST"])
def reserva():
    if "rol" in session:
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
            caducida = request.form['caducidad']
            
            if utils.isEmailValid(correo):
                if checkin == checkout:
                    flash('Las fechas de entrada y salida no pueden ser iguales')
                    return render_template('reserva.html')
                if check == 'hotel':
                    text =  ("Reserva realizada con exito, su tipo de pago es " + check +
                            "<br> Nos vemos en el hotel el dia " + checkin)
                    return text
                elif check == 'tarjeta':
                    text =  ("Reserva realizada con exito, su tipo de pago es " + check +
                            "<br> Nos vemos en el hotel el dia " + checkin)
                    return text
            else:
                return "<h1>Error al realizar la reserva</h1>"
    else:
        flash("Accion no permita por favor inicie sesión")
        return render_template('error.html')

#jesus

@app.route("/misHabitaciones")
def mishabitaciones():
    if "rol" in session:
        return render_template("gestion_comentarios.html")
    else:
        flash("Accion no permita por favor inicie sesión")
        return render_template('error.html')




if __name__ == '__main__':
    app.run(debug=True, port=8000)
