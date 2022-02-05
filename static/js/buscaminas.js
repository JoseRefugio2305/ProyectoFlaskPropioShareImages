    let filas=15;
    let columnas=20;
    let lado=30;
    let vidas=3;
    let  marcas=0;
    let timevalue=0;

    var soundLoseLive = new Howl({
      src: ['/static/music/error.mp3'],
      volume: 10.0
    });
    var soundLoseGame2 = new Howl({
      src: ['/static/music/lose2.mp3'],
      volume: 10.0
    });
    var soundLoseGame3 = new Howl({
      src: ['/static/music/lose3.mp3'],
      volume: 10.0
    });
    var soundLoseGame = new Howl({
      src: ['/static/music/loser.mp3'],
      volume: 10.0
    });
    var soundWin = new Howl({
      src: ['/static/music/victoria.mp3'],
      volume: 10.0
    });

    let contadortiempo=1

    let minas=filas*columnas*0.1

    let tablero=[]

    let enJuego=true//para saber si el juego ha terminado
    let juegoIniciado=false//saber cuando el usuario ha dado clic sobre el tablero lo que quiere decri que inicio el juego

    nuevoJuego()
    function nuevoJuego(){
        document.getElementById("tiempo").innerHTML="<i class='fas fa-stopwatch'></i> 000"
        document.getElementById('vidas').innerHTML="<i class='fas fa-heart'></i> 3"
        soundLoseGame.stop()
        soundLoseGame2.stop()
        soundLoseGame3.stop()
        soundWin.stop()
        clearInterval(timevalue)
        soundLoseLive.stop()
        reiniciarVariables()
        generarTableroHTML()
        anadirEventos()
        generarTableroJuego()
        refrescarTablero()
    }

    async function ajustes() {
        const {
            value: ajustes
        } = await swal.fire({
        title: "Ajustes",
        html: `
                Dificultad &nbsp; (minas/área)
                <br>
                <br>
                <input onchange="cambiarValor()" oninput="this.onchange()" id="dificultad" type="range" min="10" max="40" step="1" value="${100 * minas / (filas * columnas)}" onchange="">
                <span id="valor-dificultad">${100 * minas / (filas * columnas)}%</span>
                <br>
                <br>
                Filas
                <br>
                <input class="swal2-input" type="number" value=${filas} placeholder="filas" id="filas" min="10" max="100" step="1">
                <br>
                Columnas
                <br>
                <input class="swal2-input" type="number" value=${columnas} placeholder="columnas" id="columnas" min="10" max="100" step="1">
                <br>
                `,
        confirmButtonText: "Establecer",
        cancelButtonText: "Cancelar",
        showCancelButton: true,
        preConfirm: () => {
            return {
                columnas: document.getElementById("columnas").value,
                filas: document.getElementById("filas").value,
                dificultad: document.getElementById("dificultad").value
            }
            }
        })
        if (!ajustes) {
            return
        }
        filas = Math.floor(ajustes.filas)
        columnas = Math.floor(ajustes.columnas)
        minas = Math.floor(columnas * filas * ajustes.dificultad / 100)
        if(filas<=50 && columnas<=50&&filas>=10&&columnas>=10){
            nuevoJuego()
        }
        else if(filas==100&&columnas==100){
            nuevoJuego()
        }
        else{
            Swal.fire(
                'Lo sentimos',
                'El tablero tiene un limite minimo de 10x10 y un limite maximo de 50x50 o un tablero de 100x100',
                'warning'
                )
        }
    }

    function cambiarValor(){
        let valdif=document.getElementById("dificultad")
        let txtvaldif=document.getElementById("valor-dificultad")
        valdif.innerHTML=valdif.value()
    }



    function reiniciarVariables() {
        marcas=0
        enJuego=true//para saber si el juego ha terminado
        juegoIniciado=false//saber cuando el usuario ha dado clic sobre el tablero lo que quiere decri que inicio el juego
        contadortiempo=1
        vidas=3
        actualizarPanelMinas()
    }

    function generarTableroHTML(){


        let html="";
        for(let f=0;f<filas;f++){
            html+=`<tr>`
            for(let c=0;c<columnas;c++){
                /*
                    Generacion de cada uno de los elementos de la matriz
                    y se les asignara una coordenada, para poder tratar estos elementos
                    de forma matematica, siguiendo patrones que facilitara la estructura de
                    algoritmos
                    id="celda-${c}-${f}"
                    es la instruccion mas importante, esta asignara una corrdenada a cada id de las celdas
                */
                html+=`<td id="celda-${c}-${f}" style="width:${lado}px;height:${lado}px;">`
                html+=`</td>`
            }
            html+=`</tr>`
        }
        let tableroHTML=document.getElementById('tablero')
        tableroHTML.innerHTML=html
        tableroHTML.style.width=columnas*lado+'px'
        tableroHTML.style.height=filas*lado+"px"
        tableroHTML.style.background="slategray"
    }

    /*
        Acada celda se le a;aden los eventos relacionados al raton para que exista la interaccion
    */
    function anadirEventos() {
        for(let f=0;f<filas;f++){
            for(let c=0;c<columnas;c++){
                let celda = document.getElementById(`celda-${c}-${f}`)
                celda.addEventListener("dblclick",me=>{
                    dobleClick(celda,c,f,me)
                })
                celda.addEventListener("mouseup",me=>{
                    clicSimple(celda,c,f,me)
                })
            }
        }
    }


    /*Esta funcion destapara las celdas que rodean a la celda que se le dio doble click*/
    function dobleClick(celda,c,f,me) {
        if (!enJuego) {
            return//si no esamos en juego retornamos y no se realiza nada
        }
        abrirArea(c,f)
        refrescarTablero()
    }
    /*Se encargara de comportamiento de clic derecho e izquierdo para descubrir las celdas o
    marcarlas para protegerlas de ser descubiertas*/
    function clicSimple(celda,c,f,me){
        if (!enJuego) {
            return//si no esamos en juego retornamos y no se realiza nada
        }
        if(tablero[c][f].estado=="descubierto"){
            return//si la casilla esta descubierta ya no se hace ninguna accion sobre ella
        }
        switch (me.button) {
            case 0://codigo para clic izquierdo
                if(tablero[c][f].estado=="marcado"){
                    break//porque no se pueden abrir celdas marcadas
                }
                if(!juegoIniciado){

                    timevalue=window.setInterval(function(){

                        let timecount=document.getElementById("tiempo")
                        timecount.innerHTML="<i class='fas fa-stopwatch'></i> "+contadortiempo
                        contadortiempo++
                    },1000);
                }
                /*
                    Hay que proteger para evitar que el primer clic resulte ser una mina y termine el juego
                    inmediatamente
                */
                while(!juegoIniciado&&tablero[c][f].valor==-1){
                    //se estima que no le tomara mas de dos iteraciones arreglar el tablero de juego
                    //y cambiar esa bomba que se encontro en el primer clic
                    generarTableroJuego()
                }
                if(tablero[c][f].valor==-1 && vidas>0)
                {

                    soundLoseLive.play()
                    vidas=vidas-1
                    let vidasPanel=document.getElementById("vidas")
                    vidasPanel.innerHTML="<i class='fas fa-heart'></i> "+vidas
                    if(filas==100&&columnas==100)
                    {
                        Swal.fire(
                        ':(',
                        'Perdiste una vida te quedan '+vidas+' vidas',
                        'error'
                        )
                    }
                }
                else
                {
                    tablero[c][f].estado="descubierto"
                }

                juegoIniciado=true//aqui se avisa que el jugador ya descubrio al menos una celda por lo que el juego inicio

                if(tablero[c][f].valor==0){
                    //si encontramos una celda sin minas alrededor, lo que se hac es despejar el area hasta encontrar celdas
                    //con minas alrededor
                    abrirArea(c,f)
                }
                break;
            case 1://codigo para el clic medio o scroll
                //talvez no se utilise
                break;
            case 2://codigo para clic derecho
                if(tablero[c][f].estado=="marcado"){
                    tablero[c][f].estado=undefined
                    marcas--
                }else{
                    tablero[c][f].estado="marcado"
                    marcas++
                }
                break;
            default:
                break;
        }
        refrescarTablero()
    }


    function abrirArea(c,f) {
        //se recorren las celdas de alrededor
        for (let i = -1; i <= 1; i++) {
            for (let j = -1; j <= 1; j++) {
                if(i==0&&j==0){
                    continue//para que no se encierre en un bucle infinito
                }
                try {//nos cuidamos de posiciones negativas
                    if(tablero[c+i][f+j].estado!="descubierto"){
                        if(tablero[c+i][f+j].estado!="marcado"){
                            tablero[c+i][f+j].estado="descubierto"
                            if(tablero[c+i][f+j].valor==0){
                                abrirArea(c+i,f+j)
                            }
                        }
                    }
                } catch (error) {

                }
            }
        }
    }

    function refrescarTablero() {
        for(let f=0;f<filas;f++){
            for(let c=0;c<columnas;c++){
                let celda = document.getElementById(`celda-${c}-${f}`)
                if(tablero[c][f].estado=="descubierto")
                {
                    celda.style.boxShadow="none"
                    switch (tablero[c][f].valor) {
                        case -1:
                            celda.innerHTML = '<i class="fas fa-bomb"></i>'
                            celda.style.color="red"
                            celda.style.background="black"
                            break;
                        case 0:
                            break;
                        default:
                            celda.innerHTML = tablero[c][f].valor
                            break;
                    }
                }
                if(tablero[c][f].estado=="marcado"){
                    celda.innerHTML = '<i class="fas fa-flag"></i>'
                    celda.style.background="cadetblue"
                }
                if(tablero[c][f].estado==undefined){
                    celda.innerHTML = ''
                    celda.style.background=""
                }
            }
        }
        verificarPerdedor()
        verificarGanador()
        actualizarPanelMinas()
    }

    function actualizarPanelMinas() {
        let Panel=document.getElementById("minas")
        Panel.innerHTML="<i class='fas fa-flag'></i> "+(minas-marcas)
    }

    function verificarGanador() {
        /*se verfica que las minas esten totalmente tapadas y que las demas esten descubiertas*/
        for(let f=0;f<filas;f++){
            for(let c=0;c<columnas;c++){
                if(tablero[c][f].estado!="descubierto"){//si la mina esta cubierta
                    if(tablero[c][f].valor==-1){//y es una mina
                        continue//vamos bien
                    }
                    else{
                        return//si encuentra una celda buerta que no es una mina aun no se ha ganado
                    }
                }
            }
        }
        soundWin.play()
        //si al finalizar la comprobacion, todas las celdas cubiertas son minas, entonces se ha ganado
        let tableroHTML=document.getElementById("tablero")
        tableroHTML.style.background="green"
        enJuego=false
        clearInterval(timevalue)
        data=[contadortiempo,Math.floor((minas/(columnas * filas ))*100),filas,columnas]
        $.getJSON('/puntajeGanador/'+data, function(data){

                Swal.fire(
                data.titlemessage,
                data.message,
                data.messagetype
                )
            });
    }
    function verificarPerdedor() {

        for(let f=0;f<filas;f++){
            for(let c=0;c<columnas;c++){
                //si hay una mina descubierta quiere decir que el jugador perdio
                if(tablero[c][f].valor==-1){
                    if(tablero[c][f].estado=="descubierto"){
                    let tableroHTML=document.getElementById("tablero")
                    tableroHTML.style.background="red"
                    let vidasPanel=document.getElementById("vidas")
                    vidasPanel.innerHTML="<i class='fas fa-heart-broken'></i> "+vidas

                    enJuego=false
                    var x=Math.floor(Math.random()*3);
                    if(x==1)
                    {
                        soundLoseGame.play()
                    }
                    else if(x==0){
                        soundLoseGame2.play()
                    }
                    else{
                        soundLoseGame3.play()
                    }
                    Swal.fire({
                        title: 'Custom width, padding, color, background.',
                        width: 600,
                        padding: '3em',
                        color: '#716add',
                        background: '#fff url(/images/trees.png)',
                        backdrop: `
                            rgba(0,0,123,0.4)
                            url("/images/nyan-cat.gif")
                            left top
                            no-repeat
                            `
                        })

                    }
                }
            }
        }
        if(enJuego){
            return
        }
        for(let f=0;f<filas;f++){
            for(let c=0;c<columnas;c++){
                if(tablero[c][f].valor==-1){
                    let celda = document.getElementById(`celda-${c}-${f}`)
                    celda.innerHTML = '<i class="fas fa-bomb"></i>'
                    celda.style.color="white"
                }
            }
        }
        clearInterval(timevalue)
        Swal.fire(
                'Lo sentimos',
                'Perdiste',
                'error'
        )
    }

    /*generar tablero de juego no de html, este servira para dar seguiemeinto logico de los elementos
    que el jugador no puede ver*/
    function generarTableroJuego(){
        vaciarTablero()//vaciar tablero para evitar interferencias de partidas pasadas
        ponerMinas()//las minas seran representadas por el numero -1
        contadoresMinas()//contadres d minas
    }

    //resetea el tablero
    function vaciarTablero() {
        tablero=[]
        for (let c = 0; c < columnas; c++) {
            tablero.push([])
        }
    }
    function ponerMinas() {
        for (let i = 0; i < minas; i++) {
            let c
            let f
            do {
                c=Math.floor(Math.random()*columnas)//genera una columna aleatoria
                f=Math.floor(Math.random()*filas)
            } while (tablero[c][f]);//se encarga de verificar que en la celda no haya una mina
            tablero[c][f]={valor:-1}//se inserta la mina en la celda disponible en forma de parametro, para que la celda se comporte en forma de objeto
        }
    }
    function contadoresMinas() {
        for(let f=0;f<filas;f++){
            for(let c=0;c<columnas;c++){
                if(!tablero[c][f]){
                    let contador=0
                    //se recorren las celdas de alrededor
                    for (let i = -1; i <= 1; i++) {
                        for (let j = -1; j <= 1; j++) {
                            if(i==0&&j==0){
                                continue//esto es cuando ambas tienen este valor la celda se cuenta
                                //a si misma y eso no  tiene sentido asi que pasamos
                            }
                            try {//evitamos errores con las posiciones negativas
                                if(tablero[c+i][f+j].valor==-1){
                                    contador++
                                }
                            } catch(e) {

                            }
                        }
                    }
                    tablero[c][f]={valor:contador}
                }
            }
        }
    }