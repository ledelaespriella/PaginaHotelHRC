
function guardarHab(){
    document.getElementById("formulario").action="/admin/panelAdm/gestionHab/agregarH"
}

function consultarHab(){
    document.getElementById("formulario").action="/admin/panelAdm/gestionHab/get"
}

function listarHab(){
    document.getElementById("formulario").action="/admin/panelAdm/gestionHab/lista"
}

function actualizarHab(){
    document.getElementById("formulario").action="/admin/panelAdm/gestionHab/editarH"
}

function eliminarHab(){
    document.getElementById("formulario").action="/admin/panelAdm/gestionHab/eliminarH"
}