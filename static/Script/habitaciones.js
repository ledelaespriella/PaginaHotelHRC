function Buscar() {
    var habitaciones = ["101", "102", "103", "104", "105"];
    document.getElementsByClassName('predeterminado')[0].style.display = 'none';
    var y = document.getElementById('id');
    var busHab = habitaciones.includes(y.value);
    if (!busHab) {
        alert("Habitacion no existente, pruebe nuevamente");
    }
    else{
        var x = document.getElementsByClassName('mostrar');
        var i;
        for (i = 0; i < x.length; i++) {
            x[i].style.display = 'none';
        }
        document.getElementById(y.value).style.display = 'inline';
    }
}

function Mostrar() {
    var x = document.getElementsByClassName('mostrar');
    var i;
    for (i = 0; i < x.length; i++) {
        x[i].style.display = 'inline';
    }
    document.getElementById('btn2').style.display = 'none';
    document.getElementById('btn3').style.display = 'inline';
}

function Ocultar() {
    var x = document.getElementsByClassName('mostrar');
    var i;
    for (i = 0; i < x.length; i++) {
        x[i].style.display = 'none';
    }
    document.getElementById('btn2').style.display = 'inline';
    document.getElementById('btn3').style.display = 'none';
}
