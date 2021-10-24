let gestionHab=document.getElementById("gestHab");
let nav = document.getElementById("nav");

gestionHab.addEventListener("mouseover",gest_hab);


function eliminar(){
    var btnElim = document.getElementById("eliminarHab").action="/admin/panelAdm";
}

function gest_hab(){
    nav.classList.toggle("mostrar");
    alert("Alerta de eventos");
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