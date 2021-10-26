
function guardarHab(){
    document.getElementById("formulario").action="/admin/panelAdm/gestionHab/agregarH"
}

function consultarHab(){
    document.getElementById("formulario").action="/admin/panelAdm/gestionHab/get"
}

function Habitaciones_list(){
    document.getElementById("formulario").action="/habitaciones/list"
}

function actualizarHab(){
    document.getElementById("formulario").action="/admin/panelAdm/gestionHab/editarH"
}

function eliminaMsjH(){
    document.getElementById("formulario").action="/admin/panelAdm/gestionHab/msjeliminarH"
}

function eliminarHab(){
    document.getElementById("formularioE").action="/admin/panelAdm/gestionHab/eliminarH"
}