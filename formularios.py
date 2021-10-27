from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
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