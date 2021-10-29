function obtener(elemento,rol_u){ 

    document.getElementById("usuario_s").value=elemento;
    document.getElementById("rol_usuario").value=rol_u;
}

function eliminar(){ 
    document.getElementById("formulario_u").action="/admin/panelAdm/gestion_usuarios/delete"
}
function actualizar(){ 

    document.getElementById("formulario_u").action="/admin/panelAdm/gestion_usuarios/up"
}

