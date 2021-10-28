function limpiar(){
    document.getElementById("estadoHab").checked = false;
    document.getElementById("numHab").value="";

}
function deshCheck(){
    document.getElementById("estadoHab").checked = false;
}

function clearNum(){
    document.getElementById("numHab").value="";
}


function buscarHab(){
    var numHab = document.getElementById("numHab").value;
    if (!numHab==""){
        deshCheck()
        document.getElementById("formulario").action="/habitaciones/get"
    }
    else{
        document.getElementById("formulario").action="/habitaciones/disp"
    }

}
function listarHab(){
    document.getElementById("formularios").action="/habitaciones/list"
    limpiar()
}

function ocultarHab(){
    document.getElementById("formulario").action="/habitaciones"
    limpiar()
}



