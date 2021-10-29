function obtener(elemento, comentario){ 

    document.getElementById("hab_a_comentar").value=elemento;
    if(comentario!="None"){
        document.getElementById("comentario_hab").value=comentario;
        document.getElementById("actualizar-comentario").style.display="block"
        document.getElementById("enviar_comentario").style.display="none"
        document.getElementById("eliminar_comentario").style.display="block"
  
    }
    else{
        document.getElementById("comentario_hab").value="";
        document.getElementById("actualizar-comentario").style.display="none"
        document.getElementById("enviar_comentario").style.display="block"
        document.getElementById("eliminar_comentario").style.display="none"
      
    }
    }
function guardar(){ 
    document.getElementById("formulario").action="/misHabitaciones/save"
    
}
function eliminar(){ 
  
    document.getElementById("formulario").action="/misHabitaciones/delete"
}
function actualizar(){ 

    document.getElementById("formulario").action="/misHabitaciones/up"
}

