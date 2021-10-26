var x = document.getElementById('arrow');

x.addEventListener('click', function(){
    document.getElementById('menu').style.display = 'block';
})

document.getElementById('menu').addEventListener('mouseover', function(){
    
    document.getElementById('menu').style.display = 'none';
})