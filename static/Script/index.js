function validarRecuperacion() {
    
    var email=document.formRecuperacion.correo;

    var formatoCorreo = /^[-\w.%+]{1,64}@(?:[A-Z0-9-]{1,63}\.){1,125}[A-Z]{2,63}$/i;
    if(!email.value.match(formatoCorreo)){
        alert("Debes ingresar un correo electronico válido");
        correo.focus();
    }
}

function validarRegistro() {
    
    var email=document.formRegistro.email;
    var pas1=document.formRegistro.pass;
    var pas2=document.formRegistro.passVer;

    var formatPass= /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&.])[A-Za-z\d@$!%*?&.]{8,}$/i;
    var formatoCorreo = /^[-\w.%+]{1,64}@(?:[A-Z0-9-]{1,63}\.){1,125}[A-Z]{2,63}$/i;
    if(!email.value.match(formatoCorreo)){
        alert("Debes ingresar un correo electronico válido");
    }

    if(!pas1.value.match(formatPass)){
        alert("Error el crear contraseña. Debes ingresar una contraseña con las siguientes caracteristicas:\n\n-Minimo 1 letra mayuscula\n-Minimo 1 letra Miniscula\n-Minimo 1 caracter especial\n-Minimo 1 numero\n-Tamaño minimo de 8 caracteres")
    }

    if (pas1.value != pas2.value) {
        alert("Las coontraseñas deben de coincidir");
    }

}


window.addEventListener("load", function() {

    // icono para mostrar contraseña
    showPassword = document.querySelector('.show-password');
    showPassword.addEventListener('click', () => {

        // elementos input de tipo clave
        password1 = document.querySelector('.password1');
        password2 = document.querySelector('.password2');

        if ( password1.type === "text" ) {
            password1.type = "password"
            password2.type = "password"
            showPassword.classList.remove('fa-eye-slash');
        } else {
            password1.type = "text"
            password2.type = "text"
            showPassword.classList.toggle("fa-eye-slash");
        }

    })

});

function validarContrasena() {

    var pas1=document.formularioRecuperacionPassw.pass;
    var pas2=document.formularioRecuperacionPassw.passVer;

    var formatPass= /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&.])[A-Za-z\d@$!%*?&.]{8,}$/i;

    if(!pas1.value.match(formatPass)){
        alert("Error el crear contraseña. Debes ingresar una contraseña con las siguientes caracteristicas:\n\n-Minimo 1 letra mayuscula\n-Minimo 1 letra Miniscula\n-Minimo 1 caracter especial\n-Minimo 1 numero\n-Tamaño minimo de 8 caracteres")
    }

    if (pas1.value != pas2.value) {
        alert("Las contraseñas deben de coincidir");
    }

}
