from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Length, Email
from wtforms.fields.html5 import EmailField


class FormLogin(FlaskForm):
    
    correo = EmailField('usuario', validators=[DataRequired(message='No dejar vacio') ],render_kw={'placeholder':'name@example.com', 'class':'form-control'})
    contrasena = PasswordField('contrasena', validators=[DataRequired(message='No dejar vacio')],render_kw={'placeholder':'Contraseña', 'class':'form-control'})
    enviar= SubmitField('Iniciar sesion', render_kw={'onmouseover':'validarLogin()','class':'w-100 btn btn-lg btn-primary'})
    
class FormRegistro(FlaskForm):
    Primer_nombre =StringField('Primer nombre', validators=[DataRequired(message='No dejar vacio')],render_kw={'placeholder':'Primer nombre','class':'form-control'})
    Segundo_nombre=StringField('Segundo nombre', render_kw={'placeholder':'Segundo nombre','class':'form-control'})
    Primer_apellido=StringField('Primer apellido', validators=[DataRequired(message='No dejar vacio')],render_kw={'placeholder':'Primer apellido','class':'form-control'})
    Segundo_apellido=StringField('Segundo apellido', render_kw={'placeholder':'Segundo apellido','class':'form-control'})
    correo=EmailField('Correo', validators=[DataRequired(message='No dejar vacio')],render_kw={'placeholder':'Correo electronico','class':'form-control','id':'email'})
    identificacion=StringField('Identificacion', validators=[DataRequired(message='No dejar vacio')],render_kw={'placeholder':'Identificación','class':'form-control'})
    contrasena=PasswordField('Contraseña', validators=[DataRequired(message='No dejar vacio')],render_kw={'placeholder':'Contraseña','class':'form-control','id':'pass'})
    confirmacion_contrasena=PasswordField('Confirmar contraseña', validators=[DataRequired(message='No dejar vacio')],render_kw={'placeholder':'Confirmar contraseña','class':'form-control','id':'passVer'})
    enviar_registro=SubmitField('Registrarse',render_kw={'onclick':'validarRegistro()','class':'btn btn-lg btn-primary'})

class FormCrearHab(FlaskForm):
    nomHabitacion = StringField('Nombre', validators=[DataRequired(message='No dejar vacío')], render_kw={'placeholder':'Nombre de Habitación','class':'form_control'})
    idHabitacion = StringField('Id', validators=[DataRequired(message='No dejar vacío')], render_kw={'placeholder':'Id de Habitación','class':'form_control'})

    guardar = SubmitField('Guardar', render_kw={'onclick':'guardarHab()', 'class':'form_boton'})
    salir = SubmitField('Salir', render_kw={'onclick':'guardarHab()', 'class':'form_boton'})
