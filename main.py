from formularios import FormLogin
import os
import utils
from flask import Flask, request, flash
from flask import render_template
from flask.helpers import url_for
from werkzeug.utils import redirect
import yagmail

app = Flask(__name__)
app.secret_key = os.urandom(24)

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
            if(user != "luisdelaespriellaj@hotmail.com" or user != "admin@gmail.com"):
                flash('Usuario incorrecto')
            else:
                flash('Verifique la contraseña e intente nuevamente')
            return render_template('login.html',form=form)
        
    else:
        return render_template('login.html',form=form)



@app.route('/registro', methods=['GET', 'POST'])
def registro():

    try:
        if request.method == 'POST':
            correo = request.form["email"]
            passw = request.form["password"]
            error = None

            if not utils.isEmailValid(correo):
                error = "Correo invalido."
                flash(error)
                return render_template("registro.html")

            if not utils.isPasswordValid(passw):
                error = "Contraseña invalida por favor registre una correcta."
                flash(error)
                return render_template("registro.html")

            yag = yagmail.SMTP("pruebasluismintic", "Darkluise2")
            yag.send(to=correo, subject="Activa tu cuenta",contents="Bienvenido, usa este link para activar tu cuenta")
            flash("Revisa tu correo para activar tu cuenta")
            return redirect(url_for("login"))
        else:
            return render_template('registro.html')
    except:
        return render_template('registro.html')
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
            return redirect(url_for("mensaje"))
            

    else:
        return render_template('recuperacion.html')


@app.route('/login/recuperacion/mensaje', methods=['GET', 'POST'])
def mensaje():
    return render_template('mensaje.html')


@app.route('/habitaciones', methods=['GET', 'POST'])
def pagina():
    
    return render_template('habitaciones.html')

@app.route('/admin/habitaciones', methods=['GET', 'POST'])
def pagina_admin():
    admin="admin@gmail.com"
    
    return render_template('habitaciones.html',usuario=admin)

@app.route('/admin/dashboard', methods=['GET', 'POST'])
def pagina_prueba():
    return render_template('prueba.html')


if __name__ == '__main__':
    app.run(debug=True, port=8000)
