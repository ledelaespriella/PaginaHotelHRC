function limpiar(){
    console.log('Se limpio')
    var r1 = document.getElementById('radio1')
    var r2 = document.getElementById('radio2')
    var r3 = document.getElementById('radio3')
    var r4 = document.getElementById('radio4')
    var r5 = document.getElementById('radio5')

    var radios = [r1, r2, r3, r4, r5]
    for(var i = 0; i < radios.length; i++ ){
        radios[i].checked = false
        document.getElementById('cali').textContent = '0.0'
    }
    
}

function enviar(){
    var r1 = document.getElementById('radio1')
    var r2 = document.getElementById('radio2')
    var r3 = document.getElementById('radio3')
    var r4 = document.getElementById('radio4')
    var r5 = document.getElementById('radio5')

    var radios = [r1, r2, r3, r4, r5]
    for(var i = 0; i < radios.length; i++ ){
        if (radios[i].checked == true ){
            document.getElementById('cali').textContent = parseFloat(radios[i].value)
        }
        
    }
    
}