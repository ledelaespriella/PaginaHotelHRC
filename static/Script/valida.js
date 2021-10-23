function eliminar(){
    var btnElim = document.getElementById("eliminarHab").action="/admin/panelAdm";
}

function gestionHab(){
    var btnHab = document.getElementById("gestHab");
}

function agregarH(){
    var btnAdd = document.getElementById("newHab").action="/habitaciones";
}
function guardar(){
    var btnAdd = document.getElementById("guardar").action="/habitaciones";
}
function editarH(){
    var btnEdit = document.getElementById("editHab").action="/admin/panelAdm/gestionHab/editarHab";
    var btnElim = document.getElementById("eliminarHab").action="/admin/panelAdm/gestionHab/eliminarH";
}