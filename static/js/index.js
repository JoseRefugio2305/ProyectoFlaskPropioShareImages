//
    
function LikeCangeIndx(idpub)
{
    if($('#iconlikeindx'+idpub).is('.far'))
    {
        
        $.getJSON('/like/'+idpub+'.like', function(data){
            if(data.islike)
            {
                $('#iconlikeindx'+idpub).removeClass('far fa-heart');
                $('#iconlikeindx'+idpub).addClass('fas fa-heart');
                document.getElementById('btnlikeindx'+idpub).style.color='red';
                $("#contadorlikesindx"+idpub).html("<b> Me gusta "+data.likejson[0]+"</b>");
            }
            else
            {
                Swal.fire(
                'Oops!',
                'No puedes reaccionar a publicaciones si no has creado una cuenta',
                'error'
                )
            }
            
        });
    }
    else{
        
        $.getJSON('/like/'+idpub+'.dislike', function(data){
            
            if(data.islike)
            {
                $('#iconlikeindx'+idpub).removeClass('fas fa-heart');
                $('#iconlikeindx'+idpub).addClass('far fa-heart');
                document.getElementById('btnlikeindx'+idpub).style.color='black';
                $("#contadorlikesindx"+idpub).html("<b> Me gusta "+data.likejson[0]+"</b>");
            }
            else
            {
                Swal.fire(
                'Oops!',
                'No puedes reaccionar a publicaciones si no has creado una cuenta',
                'error'
                )
            }
        });
    }
}
//estas variable de conteo funcionan para saber cuantas veces he lleegado al final de la ventana
var cont=1;//para que solo llame a la ruta json una vez
var cont2=1;//saber cantas veces se han cargado mpublicaciones en la pag
//con este metodo se puede saber cuando se llegaal final de la pagina
$(window).on("scroll", function() {
    
    var scrollHeight = $(document).height();
    var scrollPosition = $(window).height() + $(window).scrollTop();
    if ((scrollHeight - scrollPosition) / scrollHeight === 0 && cont==1) {
    document.getElementById('divcargandopubs').style.display='';
    versvg();
    $.getJSON('/getMorePublics/1.'+(cont2*20), function(data){
        
        cont=2;
        cont2+=1;
        if(data.publications.length>0)
        {    var html='';
            
            data.publications.forEach(publication=>{
            if(data.is_connected)
            {
                
                html="<div class=''>"+
                    "<div class='card' >"+
                        "<img src='"+publication[3]+"'height='200' width='500' class='card-img-top img-fluid' alt='"+publication[1]+"'>"+
                        "<div class='card-body'>"+
                            "<h5 class='card-title' style='text-overflow: ellipsis; overflow: hidden;white-space: nowrap;'>"+publication[1]+"</h5>"+
                        "</div>"+
                        "<div class='card-footer'>"+

                            "<div class='row'>";
                                    if(publication[8]==1)
                                    {
                                        html+="<a class='btn col-md-12' id='btnlikeindx"+publication[0]+"' style='color: red;'onclick='LikeCangeIndx(`"+publication[0]+"`)'>";
                                            if(publication[7]==0)
                                            {
                                                html+="<i class='fas fa-heart' id='iconlikeindx"+publication[0]+"'></i> <div  id='contadorlikesindx"+publication[0]+"'> <b>  Me gusta</b></div></a>";
                                            }
                                            else
                                            {
                                                html+="<i class='fas fa-heart' id='iconlikeindx"+publication[0]+"'></i> <div  id='contadorlikesindx"+publication[0]+"'> <b>  Me gusta "+publication[7]+"</b></div></a>";
                                            }
                                    }
                                    else
                                    {
                                        html+="<a class='btn col-md-12' id='btnlikeindx"+publication[0]+"' onclick='LikeCangeIndx(`"+publication[0]+"`)'>";
                                            if(publication[7])
                                            {
                                                html+="<i class='far fa-heart' id='iconlikeindx"+publication[0]+"'></i> <div  id='contadorlikesindx"+publication[0]+"'> <b>  Me gusta</b></div></a>";
                                            }
                                            else
                                            {
                                                html+="<i class='far fa-heart' id='iconlikeindx"+publication[0]+"'></i> <div  id='contadorlikesindx"+publication[0]+"'> <b>  Me gusta "+publication[7]+"</b></div></a>";
                                            }
                                    }
                                    
                           html+=" </div>"+
                            "<div class='row'>"+
                                "<a class='btn col-md-12' href='/publication/"+publication[0]+"'>"+
                                    "<i class='far fa-eye'></i> <b>Ver Publicacion</b>"+
                                "</a>"+
                           " </div>"+
                       " </div>"+
                   " </div>"+
               " </div>";
            }
            else
            {
                html="<div class=''>"+
                    "<div class='card' >"+
                        "<img src='"+publication[3]+"'height='200' width='500' class='card-img-top img-fluid' alt='"+publication[1]+"'>"+
                        "<div class='card-body'>"+
                            "<h5 class='card-title' style='text-overflow: ellipsis; overflow: hidden;white-space: nowrap;'>"+publication[1]+"</h5>"+
                        "</div>"+
                        "<div class='card-footer'>"+

                            "<div class='row'>"+
                                                
                                "<a class='btn col-md-12' id='btnlikeindx"+publication[0]+"'nclick='LikeCangeIndx(`"+publication[0]+"`)'>";
                                
                                if(publication[7]==0)
                                {
                                    html+="<i class='far fa-heart' id='iconlikeindx"+publication[0]+"'></i> <div  id='contadorlikesindx"+publication[0]+"'> <b>  Me gusta</b></div></a>";
                                }
                                else
                                {
                                    html+="<i class='far fa-heart' id='iconlikeindx"+publication[0]+"'></i> <div  id='contadorlikesindx"+publication[0]+"'> <b>  Me gusta "+publication[7]+"</b></div></a>";
                                }
                           html+=" </div>"+
                            "<div class='row'>"+
                                "<a class='btn col-md-12' href='/publication/"+publication[0]+"'>"+
                                    "<i class='far fa-eye'></i> <b>Ver Publicacion</b>"+
                                "</a>"+
                           " </div>"+
                       " </div>"+
                   " </div>"+
               " </div>";
            }
            console.log(1)
            document.getElementById('containerpublics').innerHTML=document.getElementById('containerpublics').innerHTML+html;
            cont=1;
            });
            document.getElementById('divcargandopubs').style.display='none';
        }
        else
        {
            document.getElementById('divcargandopubs').style.display='none';
            
        }
    });
    
}
});
/*
window.addEventListener('resize', function(e){
    console.log('gola');
    if (window.innerWidth>767 && window.innerWidth<1001){
        console.log(window.innerWidth);
    }
})*/
var idinterval;//funcionara para guardar el id del intervalo de tiempo y terminar el antrior antes de iniciar el
//siguiente intervalo al llamar a la funcio, si no se detiene la animacion se vera mal
function versvg(){
    clearInterval(idinterval);
    var path = document.querySelector('.marco');
    var length = path.getTotalLength();
    var pathcir = document.querySelector('.circulo');
    var lengthcir = pathcir.getTotalLength();
    // Clear any previous transition
    path.style.transition = path.style.WebkitTransition = 'none';
    // Set up the starting positions
    path.style.strokeDasharray = length + ' ' + length;
    path.style.strokeDashoffset = length;
    // Trigger a layout so styles are calculated & the browser
    // picks up the starting position before animating
    path.getBoundingClientRect();
    // Define our transition
    path.style.transition = path.style.WebkitTransition =
    'stroke-dashoffset 3s ease-in-out';
    path.style.strokeDashoffset = '0';

    pathcir.style.transition = pathcir.style.WebkitTransition = 'none';
    // Set up the starting positions
    pathcir.style.strokeDasharray = lengthcir + ' ' + lengthcir;
    pathcir.style.strokeDashoffset = lengthcir;
    // Trigger a layout so styles are calculated & the browser
    // picks up the starting position before animating
    pathcir.getBoundingClientRect();
    // Define our transition
    pathcir.style.transition = pathcir.style.WebkitTransition =
    'stroke-dashoffset 3s ease-in-out';
    pathcir.style.strokeDashoffset = '0';

    idinterval=setInterval(() => {
    // Clear any previous transition
    
    path.style.transition = path.style.WebkitTransition = 'none';
    // Set up the starting positions
    path.style.strokeDasharray = length + ' ' + length;
    path.style.strokeDashoffset = length;
    // Trigger a layout so styles are calculated & the browser
    // picks up the starting position before animating
    path.getBoundingClientRect();
    // Define our transition
    path.style.transition = path.style.WebkitTransition =
    'stroke-dashoffset 3s ease-in-out';
    path.style.strokeDashoffset = '0';

    pathcir.style.transition = pathcir.style.WebkitTransition = 'none';
    // Set up the starting positions
    pathcir.style.strokeDasharray = lengthcir + ' ' + lengthcir;
    pathcir.style.strokeDashoffset = lengthcir;
    // Trigger a layout so styles are calculated & the browser
    // picks up the starting position before animating
    pathcir.getBoundingClientRect();
    // Define our transition
    pathcir.style.transition = pathcir.style.WebkitTransition =
    'stroke-dashoffset 3s ease-in-out';
    pathcir.style.strokeDashoffset = '0';
    }, 3000);
}