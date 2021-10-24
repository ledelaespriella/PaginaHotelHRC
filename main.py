from formularios import FormLogin,FormRegistro
import os
import utils
from flask import Flask, request, flash
from flask import render_template
from flask.helpers import url_for
from werkzeug.utils import redirect
import yagmail

app = Flask(__name__)
app.secret_key = os.urandom(24)

#luis
@app.route('/', methods=['GET'])
def inicio():
    return render_template('Home.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    form= FormLogin()
    
    if(form.validate_on_submit()):
        user = form.correo.data
        password = form.contrasena.data
        
        if (user == "luisdelaespriellaj@hotmail.com" and password == "Darkluise2*"):
            return redirect(url_for("pagina"))
        elif (user=="admin@gmail.com" and password == "admin1234*"):
            return redirect(url_for("pagina_admin"))
        else:
            if(user != "luisdelaespriellaj@hotmail.com"):
                flash('Usuario incorrecto')
            else:
                flash('Verifique la contraseña e intente nuevamente')
            return render_template('login.html',form=form)
        
    else:
        return render_template('login.html',form=form)  


@app.route('/registro', methods=['GET', 'POST'])
def registro():
    form=FormRegistro()
    
    try:
        if (form.validate_on_submit()):
            correo = form.correo.data
            passw = form.contrasena.data
            passwVerificacion = form.confirmacion_contrasena.data
            error = None

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
                yag = yagmail.SMTP("pruebasluismintic", "Darkluise2")
                yag.send(to=correo, subject="Activa tu cuenta",contents="Bienvenido, usa este link para activar tu cuenta")
                flash("Hola {} {} Revisa tu correo para activar tu cuenta".format(form.Primer_nombre.data,form.Primer_apellido.data))
                return redirect(url_for("login"))
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

@app.route('/habitaciones', methods=['GET', 'POST'])
def pagina():
    return render_template('habitaciones.html')

@app.route('/admin/habitaciones', methods=['GET', 'POST'])
def pagina_admin():
    admin="admin@gmail.com"
    return render_template('habitaciones.html',usuario=admin)

#rutas de adri

@app.route('/admin/panelAdm', methods=['GET'])
def panelAdm():
    admin="admin@gmail.com"
    return render_template("panel_adm.html",usuario=admin)

@app.route('/admin/panelAdm/gestionHab', methods=['GET'])
def gestionHab():
    admin="admin@gmail.com"
    return render_template('habitaciones.html',usuario=admin)

@app.route('/admin/panelAdm/gestionHab/agregarH', methods=['GET', 'POST'])
def agregarH():
    admin="admin@gmail.com"
    return render_template("agregaHab.html",usuario=admin)

@app.route('/admin/panelAdm/gestionHab/editarH', methods=['GET', 'POST']) 
def editarH():
    admin="admin@gmail.com"
    return render_template("editarHab.html",usuario=admin)

@app.route('/admin/panelAdm/gestionHab/eliminarH', methods=['GET'])
def eliminarH():
    admin="admin@gmail.com"
    return render_template("eliminar.html",usuario=admin)

#julian
@app.route('/reserva')
def load_reserva():
    return render_template('reserva.html')

@app.route('/reserva/mensaje_reserva', methods=["GET", "POST"])
def reserva():
    if request.method == 'POST':
        checkin = request.form['checkin']
        checkout = request.form['checkout']
        nombres = request.form["nombreR"]
        #apellido = request.form['apellidosR']
        correo = request.form['emailR']
        telefono = request.form['numeroR']
        preferencia = request.form['preferenciasR']
        check = request.form['typePay']
        cardName = request.form['name-card']
        cardNum = request.form['number-card']
        cvc = request.form['cvc']
        caducida = request.form['caducidad']
        titular = request.form['titular']
        
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

#jesus

@app.route("/misHabitaciones")
def mishabitaciones():
    return render_template("gestion_comentarios.html")



if __name__ == '__main__':
    app.run(debug=True, port=8000)
