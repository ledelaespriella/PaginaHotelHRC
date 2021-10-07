from flask import Flask
from flask import render_template
app=Flask(__name__)

"punto 1 y punto 2"

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

'''

@app.route('/',methods=['GET'])
def inicio():
    return render_template('inicio.html')

@app.route('/login/<usuario>',methods=['GET'])
def habitaciones(usuario):
    return render_template('habitaciones.html',user=usuario)

@app.route('/login/<usuario>/comentarios',methods=['GET','POST'])
def habitaciones(usuario):
    return render_template('comentarios.html',user=usuario)

@app.route('/login/<usuario>/reserva',methods=['GET','POST'])
def habitaciones(usuario):
    return render_template('reservas.html',user=usuario)

@app.route('/login/<usuario>/dashboard',methods=['GET','POST'])
def panel_admin(usuario):
    return render_template('panel_admin.html',user=usuario)

@app.route('/login/<usuario>/dashboard/GesHabitacion',methods=['GET','POST'])
def panel_admin(usuario):
    return render_template('gestion_habitaciones.html',user=usuario)

'''


if __name__ == '__main__':
    app.run(debug=True, port=8000)