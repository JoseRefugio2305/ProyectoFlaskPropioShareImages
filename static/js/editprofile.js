    //file es input de selección
    const $file = document.getElementById("inputGroupFile01")
    //es elemento img dentro del modal donde se montará la imagen seleccionada
    const $image = document.getElementById("img-original")

    const $modal = document.getElementById("div-modal")
        
    var modified=false;
    var imgprofilemod=false;
    var ancho = 0;
    var alto = 0;
    $(document).ready(function () 
    {   //esta parte ayuda a saber si alguno de los campos fue modificado para asi activar los botonoes de
        //guardar y cancelar
        $("input, select").change(function () {   
            modified = true;
            document.getElementById("GuardarEdicion").removeAttribute("disabled");
            document.getElementById("CancelarEdicion").removeAttribute("disabled");
        }); 
    });
    
    //document.getElementById("inputGroupFile01").onchange = function(e) {
    // Creamos el objeto de la clase FileReader
    //    let reader = new FileReader();

        // Leemos el archivo subido y se lo pasamos a nuestro fileReader
        
    //    reader.readAsDataURL(e.target.files[0]);

    //    var imagen = e.target.files[0];
    //   var _URL = window.URL || window.webkitURL;
    //    var img = new Image();
    //    img.src = _URL.createObjectURL(imagen);
    //    img.onload = function () {
    //       ancho = img.width;
    //        alto = img.height;
    //        console.log(ancho + ' ' + alto);
    //        $('#imgprofileedit').attr("src",img.src);
    //        
    //    }
    //    
    //}

    

    function validarImgProfile()
    {
        var laimgesvalida=false;
        
        if(ancho<550&&alto<550)
        {
            laimgesvalida=true;
            //console.log(laimgesvalida);
        }
        return laimgesvalida;
    }

    function validarFechaNac()
    {
        var fecha = new Date(document.getElementById("inputfechanac").value);
        var today = new Date();
        var edadyears = today.getFullYear()-fecha.getFullYear();
        var edadmonths=today.getMonth()-fecha.getMonth();
        var isfehcavalida=false;

        if(edadyears >= 18)
        {
            if(edadyears==18)
            {
                if(edadmonths>=0)
                {
                    isfehcavalida=true;
                }
            }
            else
            {
                isfehcavalida=true;
            }
        }
        return isfehcavalida;
    }

    function ConfirmEdition(){
        var imgvalida=new Boolean(false);
        if(validarFechaNac())
        {
            Swal.fire({
                title: 'Estas seguro?',
                text: "Los Cambios seran guardados!",
                icon: 'warning',
                showCancelButton: true,
                confirmButtonColor: '#3085d6',
                cancelButtonColor: '#d33',
                confirmButtonText: 'Confirmar',
                
                }).then((result) => {
                if (result.isConfirmed) {
                    document.getElementById("divformeditprofile").style.display='none';
                    document.getElementById("cargando").style.display='';
                    versvg();
                    document.getElementById("formedituser").submit();
                }
                });
        }
        else
        {
            Swal.fire({
                icon: 'warning',
                title: 'Advertencia',
                text: 'Debes de tener mas de 18 ',
            });
        }
            
        
    }

    function versvg(){
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
        'stroke-dashoffset 2s ease-in-out';
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
        'stroke-dashoffset 2s ease-in-out';
        pathcir.style.strokeDashoffset = '0';

        setInterval(() => {
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
        'stroke-dashoffset 2s ease-in-out';
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
        'stroke-dashoffset 2s ease-in-out';
        pathcir.style.strokeDashoffset = '0';
        }, 3000);
    }


    //Zona de recorte de imagen
    

    //si deseamos interactuar con el modal usando los metodos nativos de bootstrap5
    //debemos construirlo pasando el elemento. En nuestro caso .show() y .hide()
    const objmodal = new bootstrap.Modal($modal, {
        //que el modal no interactue con el teclado
        keyboard: false
    })

    //escuchamos el change del input-file
    $file.addEventListener("change", function (e) {
        const load_image = function (url){
            $image.src = url
            objmodal.show()
        }

        const files = e.target.files

        if(files && files.length>0) {
            const objfile = files[0]
            //el objeto file tiene las propiedades: name, size, type, lastmodified, lastmodifiedate
            
            //para poder visualizar el archivo de imagen lo debemos pasar a una url 
            //el objeto URL está en fase experimental así que si no existe usaria FileReader
            if (URL){
                //crea una url del estilo: blob:http://localhost:1024/129e832d-2545-471f-8e70-20355d8e33eb
                const url = URL.createObjectURL(objfile)
                load_image(url)
            }
            else if (FileReader) {
                const reader = new FileReader()
                reader.onload = function (e) {
                    load_image(reader.result)
                }
                reader.readAsDataURL(objfile)
            }
        }
    })//file.on-change


    const $btncrop = document.getElementById("btn-crop")
    //configuramos el click del boton crop
    $btncrop.addEventListener("click", function (){
        //obtenemos la zona seleccionada, ademas de eso tambien le enviamos algunas configuraciones
        //en las que bajamos la calidad de la imagen obtenida a solo 512 x 512 con un maximo de 1024
        //x1024, esto para reducir el peso de las imagenes, ya que antes de aplicar estas configuraciones
        //nos daba imagenes de varios megas de peso, y de mucha resolucion, lo cual no es necesario 
        //para una imagen de perfil que estara pequena
        
        const canvas = cropper.getCroppedCanvas({imageSmoothingQuality:'low',
                                                imageSmoothingEnabled: false,
                                                width: 512,
                                                height: 512,
                                                maxWidth: 1024,
                                                maxHeight: 1024})
        document.getElementById("contenedorimagenes").style.display="none";
        document.getElementById("divcargandoprofileimage").style.display="";
        versvg();
        canvas.toBlob(function (blob){
            //el objeto blob (binary larege object) tiene las propiedades: size y type
            const reader = new FileReader()
            //se pasa el binario base64
            reader.readAsDataURL(blob)

            reader.onloadend = function (){
                const base64data = reader.result
                //base64data es un string del tipo: data:image/png;base64,iVBORw0KGgoAAAA....
                //console.log("base64data", base64data)
                //en mi caso estoy trabajando con php en el back pero puede ser cualquier url
                const url = "/updateImgUserProfile"
                fetch(url, {
                    method: "POST",
                    headers: {
                        //si la respuesta del servidor no es un json saltará una excepción en js
                        "Accept": "application/json",
                        //le indica al servidor que se le enviará un json
                        "Content-Type": "application/json"
                    },

                    body: JSON.stringify({
                        image: base64data
                    })
                })
                .then(response => response.json())
                .then(function (result){
                    $file.value = ""    //resetea el elemento input-file (file-upload)
                    objmodal.hide()     //escondo el modal
                    document.getElementById("contenedorimagenes").style.display="";
                    document.getElementById("divcargandoprofileimage").style.display="none";
                    //result es algo como: {message:"image uploaded successfully.", file:"upload/uuid.png"}
                    Swal.fire({
                        icon: 'success',
                        title: 'Confirmacion',
                        text: result.message,
                    });

                    //este es el img que está debajo del elemnto input-file
                    const $img = document.getElementById("imgprofileedit")
                    $img.src = "/"+result.file
                })
            }//reader.on-loaded
        })//canvas.toblob
    })//btncrop.on-click


    //el objeto cropper que habrá que crearlo y destruirlo. 
    //Crearlo al mostrar el modal y destruirlo al cerrarlo
    let cropper = null
    $modal.addEventListener("shown.bs.modal", function (){
        //console.log("modal.on-show")
        //crea el marco de selección sobre el objeto $image
        cropper = new Cropper($image, {
            //donde se mostrará la parte seleccionada
            preview: document.getElementById("div-preview"),
            dragMode: 'move',
            //3: indica que no se podrá seleccionar fuera de los límites
            viewMode: 3,
            //NaN libre elección, 1 cuadrado, proporción del lado horizontal con respecto al vertical
            aspectRatio: 1,
            autoCropArea: 1,
            restore:false,
            cropBoxResizable: false,
            toggleDragModeOnDblclick: false,
        })
    })//modal.on-shown

    $modal.addEventListener("hidden.bs.modal", function (){
        //console.log("modal.on-hide")
        cropper.destroy()
        cropper = null
    })//modal.on-hidden


    var idinterval;//funcionara para guardar el id del intervalo de tiempo y terminar el antrior antes de iniciar el
    //siguiente intervalo al llamar a la funcio, si no se detiene la animacion se vera mal
    function versvg(){
    clearInterval(idinterval);
    var path = document.getElementById('marco');
    var length = path.getTotalLength();
    var pathcir = document.getElementById('circulo');
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