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

    var formatoCorreo = /^[-\w.%+]{1,64}@(?:[A-Z0-9-]{1,63}\.){1,125}[A-Z]{2,63}$/i;
    if(!email.value.match(formatoCorreo)){
        alert("Debes ingresar un correo electronico válido");
        correo.focus();
    }
}
