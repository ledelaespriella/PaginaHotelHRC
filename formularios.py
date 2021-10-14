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
    correo=EmailField('correo', validators=[DataRequired(message='No dejar vacio')],render_kw={'placeholder':'correo','class':'form-control'})
    identificacion=StringField('Identificacion', validators=[DataRequired(message='No dejar vacio')],render_kw={'placeholder':'Identificación','class':'form-control'})
    constrasena=PasswordField('Primer nombre', validators=[DataRequired(message='No dejar vacio')],render_kw={'placeholder':'Contraseña','class':'form-control'})
    confirmacion_contrasena=PasswordField('Primer nombre', validators=[DataRequired(message='No dejar vacio')],render_kw={'placeholder':'Confirm','class':'form-control'})