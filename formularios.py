from flask.templating import render_template
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Length, Email
from wtforms.fields.html5 import EmailField

class FormLogin(FlaskForm):
    correo = EmailField('usuario', validators=[DataRequired(message='No dejar vacio') ],render_kw={'placeholder':'name@example.com', 'class':'form-control'})
    contrasena = PasswordField('contrasena', validators=[DataRequired(message='No dejar vacio')],render_kw={'placeholder':'Contraseña', 'class':'form-control password1'})
    enviar= SubmitField('Iniciar sesion', render_kw={'onmouseover':'validarLogin()','class':'w-100 btn btn-lg btn-primary'})
    
class FormRegistro(FlaskForm):
    Primer_nombre =StringField('Primer nombre', validators=[DataRequired(message='No dejar vacio')],render_kw={'placeholder':'Primer nombre','class':'form-control'})
    Segundo_nombre=StringField('Segundo nombre', render_kw={'placeholder':'Segundo nombre','class':'form-control'})
    Primer_apellido=StringField('Primer apellido', validators=[DataRequired(message='No dejar vacio')],render_kw={'placeholder':'Primer apellido','class':'form-control'})
    Segundo_apellido=StringField('Segundo apellido', validators=[DataRequired(message='No dejar vacio')], render_kw={'placeholder':'Segundo apellido','class':'form-control'})
    correo=EmailField('Correo', validators=[DataRequired(message='No dejar vacio')],render_kw={'placeholder':'Correo electronico','class':'form-control','id':'email'})
    identificacion=StringField('Identificacion', validators=[DataRequired(message='No dejar vacio')],render_kw={'placeholder':'Identificación','class':'form-control'})
    contrasena=PasswordField('Contraseña', validators=[DataRequired(message='No dejar vacio')],render_kw={'placeholder':'Contraseña','class':'form-control password1','id':'pass'})
    confirmacion_contrasena=PasswordField('Confirmar contraseña', validators=[DataRequired(message='No dejar vacio')],render_kw={'placeholder':'Confirmar contraseña','class':'form-control password2','id':'passVer'})
    enviar_registro=SubmitField('Registrarse',render_kw={'onclick':'validarRegistro()','class':'btn btn-lg btn-primary'})
    
class formHabitaciones(FlaskForm):
    idHabitacion = StringField('ID', validators=[DataRequired(message='No dejar vacio')], render_kw={'placeholder':'Numero de Habitacion', 'id': 'numHab', 'class':'form_control', 'onclick':'deshCheck()'} )
    estado = BooleanField('Disponible', render_kw={ 'id': 'estadoHab', 'onclick':'clearNum()'})
    buscar = SubmitField('Buscar', render_kw={'onclick':'buscarHab()', 'class':'form_boton'} )
    listar = SubmitField('Mostrar mas habitaciones', render_kw={'onclick':'listarHab()','id':'mostar', 'class':'form_boton'} )
    ocultar = SubmitField('Mostrar menos', render_kw={'onclick':'ocultarHab()','id':'ocultar', 'class':'form_boton'} )

class formCambio_password(FlaskForm):
    contrasenaNueva=PasswordField('Contraseña Nueva', validators=[DataRequired(message='No dejar vacio')],render_kw={'placeholder':'Contraseña nueva','class':'form-control password1','id':'pass'})
    confirmacion_contrasena=PasswordField('Confirmar contraseña', validators=[DataRequired(message='No dejar vacio')],render_kw={'placeholder':'Confirmar contraseña','class':'form-control password2','id':'passVer'})
    enviar=SubmitField('Recuperar contraseña',render_kw={'onclick':'validarContrasena()','class':'btn btn-lg btn-primary'})

class formHab(FlaskForm):
    idHab = StringField('Id de Habitación', validators=[DataRequired(message='No dejar vacio')], render_kw={'placeholder':'Id de Habitación', 'class':'form_control' } )
    nomHab = StringField('Nombre de Habitación', validators=[DataRequired(message='No dejar vacio')], render_kw={'placeholder':'Nombre de Habitación', 'class':'form_control' } )
    precio = StringField('COP $', validators=[DataRequired(message='No dejar vacio')], default="250,000", render_kw={'placeholder':'Precio', 'class':'form_control' } )
    capMax = StringField('Capacidad Máxima', validators=[DataRequired(message='No dejar vacio')], default="Cap. máxima 4 personas", render_kw={'placeholder':'Capacidad máxima', 'class':'form_control' } )
    numCama = StringField('Camas', validators=[DataRequired(message='No dejar vacio')], default="2 camas tipo Queen", render_kw={'placeholder':'Número de camas', 'class':'form_control' } )
    descrip = TextAreaField('Descripción', default="Amplia habitación equipada con 2 camas Queen, closet, baño privado, TV LED, TV-Cable, Wi-Fi gratis, escritorio, minibar.", validators=[DataRequired()], render_kw={'placeholder':'Número de camas', 'class':'form_tArea' } )
    disp = BooleanField('Disponibilidad')

    guardar = SubmitField('Guardar', render_kw={'onmouseover':'guardarHab()', 'class':'form_boton'} )
    consultar = SubmitField('Consultar', render_kw={'onmouseover':'consultarHab()', 'class':'form_boton'} )
    listar = SubmitField('Listar', render_kw={'onmouseover':'listarHab()', 'class':'form_boton'} )
    actualizar = SubmitField('Actualizar', render_kw={'onmouseover':'actualizarHab()', 'class':'form_boton'} )
    eliminar = SubmitField('Eliminar', render_kw={'onmouseover':'eliminarHab()', 'class':'form_boton'} )
