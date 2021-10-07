from flask import Flask
from flask import render_template
app=Flask(__name__)

@app.route('/')
@app.route('/login',methods=['GET','POST'])
def login():
    #si ya inicio sesion -> muestra las habitaciones
    #sino -> muestra login
    return render_template('login.html')

@app.route('/registro',methods=['GET','POST'])
def registro():
    return render_template('registro.html')

@app.route('/login/recuperacion',methods=['GET','POST'])
def recuperacion():
    return render_template('recuperacion.html')

@app.route('/login/recuperacion/mensaje',methods=['GET','POST'])
def mensaje_recuperacion():
    return render_template('mensaje.html')


if __name__ == '__main__':
    app.run(debug=True, port=8000)