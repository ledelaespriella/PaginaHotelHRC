import os
import utils
from flask import Flask, request, flash
from flask import render_template
from flask.helpers import url_for
from werkzeug.utils import redirect
import yagmail

app=Flask(__name__)
app.secret_key = os.urandom(24)

#pendiente modificar todas las url locales en los templates de los static


@app.route('/', methods=['GET'])
def inicio():
    return render_template('Home.html')


@app.route('/login',methods=['GET','POST'])
def login():
    if request.method == 'POST':
        user= request.form["correo"]
        password= request.form["pass"]
        
        if user=="luisdelaespriellaj@hotmail.com" and password=="12345":
            return redirect(url_for("pagina"))
        else:
            return render_template('login.html')
    else:
        return render_template('login.html')
    
    #validar condiciones del usuario, correo electronico valido
    
    

@app.route('/registro',methods=['GET','POST'])
def registro():
    
    try:
        if request.method == 'POST':
            correo= request.form["email"]
            passw=request.form["password"]
            error=None
        
            if not utils.isEmailValid(correo):
                    error="Correo invalido."
                    flash(error)
                    return render_template("registro.html")
            
            if not utils.isPasswordValid(passw):
                    error="Contraseña invalida por favor registre una correcta."
                    flash(error)
                    return render_template("registro.html")
            
            yag=yagmail.SMTP("pruebasluismintic","Darkluise2")
            yag.send(to=correo, subject="Activa tu cuenta", contents="Bienvenido, usa este link para activar tu cuenta")
            flash("Revisa tu correo para activar tu cuenta")        
            return redirect(url_for("login"))
        else:
            return render_template('registro.html')
    except:
        return render_template('registro.html')
    #guardar en un diccionario los datos
    

@app.route('/login/recuperacion',methods=['GET','POST'])
def recuperacion():
    if request.method == 'POST':
        correo=request.form['correo']
    else:
        return render_template('recuperacion.html')

@app.route('/login/recuperacion/mensaje',methods=['GET','POST'])
def mensaje():
    return render_template('mensaje.html')

@app.route('/login/pagina')
def pagina():
    return "<h1>Pagina de prueba</h1>"

if __name__ == '__main__':
    app.run(debug=True, port=8000)