
from datetime import datetime
import os
from flask import Flask,render_template, request, redirect, session,url_for, flash, jsonify
from flask_mysqldb import MySQL
from werkzeug.utils import secure_filename
from flask_socketio import SocketIO, emit, join_room, leave_room, send

app = Flask(__name__)

#Configuraciones de MySQL
#Siempre tener activado Laragon, y la BDD esta en MySQL
app.config['MYSQL_HOST']='127.0.0.1'
app.config['MYSQL_USER']='root'
app.config['MYSQL_PASSWORD']=''
app.config['MYSQL_DB']='bddpinterestchafon'
mysql = MySQL(app)

#Session(app)

#Configuraciones de Sesion
app.secret_key = 'mysecretkey'

#configuraciones del socketio
socketiocon = SocketIO(app)

#Rutas
@app.route('/')
def home():
    
    if (is_logged()):
        cur = mysql.connection.cursor()
        cur.execute("""CALL `ConsultarPublicacionesInicioLog`({0})""".format(session["id_user"]))
        data = cur.fetchall()
        #cur2 = mysql.connection.cursor()
        #cur2.execute("SELECT p.id FROM publicacion AS p INNER JOIN reluserreaction AS rur ON p.id=rur.idPub WHERE rur.idUser={0}".format(session["id_user"]))
        cur2=mysql.connection.cursor()
        cur2.execute("CALL `PublicacionesRelevantes`()")
        data2=cur2.fetchall()
    else:
        cur = mysql.connection.cursor()
        cur.execute("""CALL `ConsultarPublicacionesInicioNoLog`()""")
        data = cur.fetchall()

        cur2=mysql.connection.cursor()
        cur2.execute("""CALL `PublicacionesRelevantes`()""")
        data2=cur2.fetchall()

    return render_template('index.html', publications = data, relevantes=data2)

#Con esta se reenderiza la plnatilla de inicio de sesion y registro
@app.route('/SiginSignup/<string:option>')
def SiginSignup(option):
    if (is_logged()):
        return redirect(url_for('home'))
    else:
        if(option.upper()=='SIGNIN'):
            login='true'
            register='false'
        else:
            login='false'
            register='true'
        return render_template('loginregister.html', showlogin=login, showreg=register)

#Esta es para llevar a cabo el registro del usuario en la BDD y lo demas necesario
@app.route('/addUser', methods=['POST'])
def addUser():
    if request.method == 'POST':#se revisa si se entro a la ruta con datos por medio del metodo POST
        #se reciben los datos ingresados en el formulario
        mensaje = ""
        messagetype=""
        email = request.form['email'].lower()
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM usuario WHERE email='{0}'".format(email))
        if (cur.fetchall()):
            mensaje='El correo ingresado ya esta siendo usado'
            messagetype='warning'
        else:
            firstname = request.form['firstname']
            lastname = request.form['lastname']
            password = request.form['password']
            genero = request.form['genero']
            date = request.form['date']

            insert = mysql.connection.cursor()
            insert.execute('CALL `INSERTnuevousuario`(%s, %s, %s, %s, %s, %s)',
            (firstname, lastname, email, password, genero, date))
            mysql.connection.commit()
            cur2 = mysql.connection.cursor()
            cur2.execute("SELECT id FROM usuario WHERE email='{0}'".format(email))
            id = cur2.fetchall()[0][0]
            session['id_user']=id
            session['email'] = email
            session['password'] = password
            session['name'] = firstname
            session['imgprofile'] = 'static/img/usernotfound.png'

            mensaje = 'El usuario fue registrado exitosamente'
            messagetype='success'

        flash(mensaje,messagetype)
        return redirect(url_for('home'))
#Esta es para llevar a cabo el logeo del usuario comprobando en la BDD y creando las sessions
@app.route('/loginUser', methods=['POST'])
def loginUser():
    if request.method == 'POST':#se revisa si se entro a la ruta con datos por medio del metodo POST
        #se reciben los datos ingresados en el formulario
        mensaje=''
        messagetype=''
        email = request.form['email'].lower()
        password = request.form['password']

        cur = mysql.connection.cursor()
        cur.execute("CALL `Loggin`(%s, %s)", (email, password))
        data = cur.fetchall()
        if(data):
            data=data[0]
            mensaje="Bienvenido de nuevo "+data[1]
            session['id_user']=data[0]
            session['password'] = password
            session['name'] = data[1]
            session['imgprofile'] = data[5]
            session['user_rol']=data[7]
            if ('/admin:' in email):
                session['email'] = email[7:]
                return redirect(url_for('AdministratorPanel',iduseradmin=session["id_user"]))
            else:
                session['email'] = email
                
            messagetype='success'
        else:
            mensaje="Correo o Contrasena incorrectos intenta de nuevo"
            messagetype='warning'
        flash(mensaje, messagetype)
        return redirect(url_for('home'))



@app.route('/UserProfile/<idprofile>')
def UserProfile(idprofile):
    data4=[0]
    if(is_logged()):
        if(str(session["id_user"])==idprofile):
            cur = mysql.connection.cursor()
            cur.execute("CALL `ConsultarDatosUsuario`({0})".format(session["id_user"]))
            data = cur.fetchall()[0]
            cur2 = mysql.connection.cursor()
            cur2.execute("""CALL `ConsultarPublicacionesDelPerfil`({0})""".format(session["id_user"]))
            data2 = cur2.fetchall()
            cur3 = mysql.connection.cursor()
            cur3.execute("""CALL `ConsultarLikesDelUsuario`({0})""".format(session["id_user"]))
            data3 = cur3.fetchall()
            cur4 = mysql.connection.cursor()
            cur4.execute("CALL `PrivatePubs`({0})".format(session["id_user"]))
            data4=cur4.fetchall()
        else:
            cur = mysql.connection.cursor()
            cur.execute("""CALL `ConsultarOtroPerfilLogged`({0}, {1})""".format(idprofile, session["id_user"]))
            data = cur.fetchall()
            if(data):
                data=data[0]
                
            cur2 = mysql.connection.cursor()
            cur2.execute("""CALL `ConsultarPublicacionesDelPerfil`({0})""".format(idprofile))
            data2 = cur2.fetchall()
            cur3 = mysql.connection.cursor()
            cur3.execute("""CALL `ConsultarLikesDelUsuario`({0})""".format(idprofile))
            data3 = cur3.fetchall()
    else:
        cur = mysql.connection.cursor()
        cur.execute("""CALL `ConsultarDatosUsuario`({0})""".format(idprofile))
        data = cur.fetchall()
        if(data):
            data=data[0]
        cur2 = mysql.connection.cursor()
        cur2.execute("""CALL `ConsultarPublicacionesDelPerfil`({0})""".format(idprofile))
        data2 = cur2.fetchall()
        cur3 = mysql.connection.cursor()
        cur3.execute("""CALL `ConsultarLikesDelUsuario`({0})""".format(idprofile))
        data3 = cur3.fetchall()
    return render_template('userprofile.html', userdata=data, userpubs = data2, userlikes = data3, userprivates = data4)


@app.route('/LogOut')
def LogOut():
    session['id_user']=None
    session['email'] = None
    session['password'] = None
    session['name'] = None    
    session['imgprofile'] = None
    session['id_conversacion']=None
    session['user_rol']=None  
    session.clear()
    return redirect(url_for('home'))

@app.route("/editProfile")
def editProfile():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM usuario WHERE email='{0}'".format(session['email']))
    data = cur.fetchall()[0]
    return render_template("editprofile.html", userdata=data)

@app.route("/updateUser", methods=["POST"])
def updateUser():
    message=""
    messagetype=""
    ruta_bdd=""
    if request.method == 'POST':
        emailedit = request.form["emailedit"]
        cur = mysql.connection.cursor()
        ##Esta es para obterner los registros donde se encuentre el mismo email, pero no el mismo id del usuario
        #es para evitar que al editar el correo usemos un correo que ya existe en otro usuario
        cur.execute("SELECT * FROM usuario WHERE email='{0}' AND id NOT LIKE {1}".format(emailedit, session['id_user']))
        if (cur.fetchall()):
            message="El correo que se ingreso ya esta siendo usado por otro usuario"
            messagetype="error"
        else:
            #Se obtiene y guarda la imagen
            imgedit = request.files["imgprofileinput"]
            if (imgedit):
                img_name_new = secure_filename( 'a'+'_'+datetime.now().strftime('%d-%m-%Y %H_%M_%S')+'_.' + imgedit.filename.split('.')[-1])
                ruta_imagen = os.path.abspath('static/img/'+str(session['id_user'])+'profile'+'/{0}'.format(img_name_new))
                ruta_bdd = 'static/img/'+str(session['id_user'])+'profile'+'/{0}'.format(img_name_new)
                os.makedirs('static/img/'+str(session['id_user'])+'profile', exist_ok=True)
                imgedit.save(ruta_imagen)
            else:
                ruta_bdd=str(session['imgprofile'])
            
            #se obtienen los demas datos
            firstnedit=request.form["firstnameedit"]
            lastnedit=request.form["lastnameedit"]
            passedit=request.form["passedit"]
            genderedit=request.form["generoedit"]
            dateedit=request.form["dateedit"]

            cur2 = mysql.connection.cursor()
            cur2.execute("""CALL `UPDATEuser`('{0}', '{1}','{2}','{3}','{4}','{5}','{6}',{7})
            """.format(firstnedit, lastnedit, emailedit, passedit, ruta_bdd, genderedit, dateedit, session['id_user']))
            mysql.connection.commit()
            message="Datos Actualizados Con Exito!"
            messagetype="success"
            #actualizamos las variables de sesion por posibles cambios
            session['email'] = emailedit
            session['password'] = passedit
            session['name'] = firstnedit
            session['imgprofile'] = ruta_bdd    


        flash(message, messagetype)
        return redirect(url_for("UserProfile", idprofile=int(session['id_user'])))

#Cada que se use este tipo de rutas en flask, en el html antes de cada ruta de algun archivo agregar una /
#si no se agrega ocurre un error en el que al principio de la ruta se agrega el nombre de la ruta flask que
#se esta usando, por lo que las imagenes no se muestran
@app.route("/publication/<pub>")
def seePublication(pub):
    #obtenemos los datos solo de la publicacion
    cur=mysql.connection.cursor()
    cur.execute("""CALL `seePublication`({0},1)""".format(pub))
    data = cur.fetchall()
    if (data):
        data=data[0]
        if(data[4]==3 and int(session['id_user'])==data[5]):
            
            #Obtenemos ahora los comentarios
            cur2=mysql.connection.cursor()
            cur2.execute("CALL `PublicationComments`({0})".format(pub))
            data2=cur2.fetchall()
            cur3=mysql.connection.cursor()
            cur3.execute("SELECT COUNT(*) FROM reluserreaction WHERE idPub={0} AND idReaction=1".format(pub))
            data3=cur3.fetchall()
            if(data3):
                data3=data3[0]
            else:
                data3=['']
            if (is_logged()):
                cur4=mysql.connection.cursor()
                cur4.execute("SELECT * FROM reluserreaction WHERE idPub={0} AND idReaction=1 AND idUser={1}".format(pub, session["id_user"]))
                data4=cur4.fetchall()
                if(len(data4)>0):
                    data4=['fas fa-heart', 'red']
                else:
                    data4=['far fa-heart', 'black']
            else:
                data4=['far fa-heart', 'black']
        if(data[4]==1):
            #Obtenemos ahora los comentarios
            cur2=mysql.connection.cursor()
            cur2.execute("CALL `PublicationComments`({0})".format(pub))
            data2=cur2.fetchall()
            cur3=mysql.connection.cursor()
            cur3.execute("SELECT COUNT(*) FROM reluserreaction WHERE idPub={0} AND idReaction=1".format(pub))
            data3=cur3.fetchall()
            if(data3):
                data3=data3[0]
            else:
                data3=['']
            if (is_logged()):
                cur4=mysql.connection.cursor()
                cur4.execute("SELECT * FROM reluserreaction WHERE idPub={0} AND idReaction=1 AND idUser={1}".format(pub, session["id_user"]))
                data4=cur4.fetchall()
                if(len(data4)>0):
                    data4=['fas fa-heart', 'red']
                else:
                    data4=['far fa-heart', 'black']
            else:
                data4=['far fa-heart', 'black']
        else:
            data2=[0]
            data3=[0]
            data4=[0]
    else:
        data2=[0]
        data3=[0]
        data4=[0]

    return render_template("publication.html", pubdata=data, pubcomments=data2, publikes=data3, userlikedata=data4)

@app.route('/like/<idpub>')
def like(idpub):
    if (is_logged()):
        idpub=str(idpub)
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM reluserreaction WHERE idPub ={0} AND idUser={1}".format(idpub.split('.')[0], session['id_user']))
        
        if (cur.fetchall()):
            cur2=mysql.connection.cursor()
            consulta=""
            if(idpub.split('.')[1]=='like'):
                consulta="""CALL `UPDATEreaccion`({0},{1}, {2})
                """.format(1,idpub.split('.')[0], session['id_user'])
            else:
                consulta="""CALL `UPDATEreaccion`({0},{1}, {2})
                """.format(2,idpub.split('.')[0], session['id_user'])
            cur2.execute(consulta)
            mysql.connection.commit()
        else:
            cur3=mysql.connection.cursor()
            consulta2=""
            if(idpub.split('.')[1]=='like'):
                consulta2="CALL `INSERTreaccion`({0}, {1}, {2})".format(session["id_user"], 1 ,idpub.split('.')[0])
            else:
                consulta2="CALL `INSERTreaccion`({0}, {1}, {2})".format(session["id_user"], 2 ,idpub.split('.')[0])
            cur3.execute(consulta2)
            mysql.connection.commit()
        cur4=mysql.connection.cursor()
        cur4.execute("SELECT COUNT(*) FROM reluserreaction WHERE idPub ={0} AND idReaction=1".format(idpub.split('.')[0], session['id_user']))
        data=cur4.fetchall()
        if data:
            data=data[0]
        else:
            data=['']
        like=True
    else:
        like=False
        data=['']
    return jsonify(likejson=data, islike=like)

@app.route('/crearPublicacion/<option>')
def crearPublicacion(option):
    if(is_logged()):
        ##Crear publicacion tambien se usacuando se quiere editar un publicacion, si resibe 0 es que se quiere crear una
        #si recibe un valor diferente quiere decir que es un id de alguna publicacion por lo que quiere editar una publicacion
        if(int(option)==0):
            data=[0]
        else:
            cur=mysql.connection.cursor()
            cur.execute("""CALL `seePublication`({0},1)""".format(option))
            data=cur.fetchall()
            if (data):
                if(int(data[0][5])==int(session["id_user"])):
                    data=data[0]
                else:
                    flash("No puedes editar publicaciones inexistentes o que fueron creadas por otro usuario", "warning")
                    return redirect(url_for('home'))
            else:
                flash("No puedes editar publicaciones inexistentes o que fueron creadas por otro usuario", "warning")
                return redirect(url_for('home'))

        return render_template('crearPublicacion.html', datapub=data)
    else:
        flash("Debes iniciar sesion para poder crear una publicacion", "warning")
        return redirect(url_for('home'))

@app.route('/addPublication', methods=["POST"])
def addPublication():
    if (request.method=="POST"):
        
        ruta_bdd=''
        #Se obtiene y guarda la imagen
        imgnewpub = request.files["imgpublication"]
        if (imgnewpub):
            img_name_new = secure_filename( 'a'+'_'+datetime.now().strftime('%d-%m-%Y %H_%M_%S')+'_.' + imgnewpub.filename.split('.')[-1])
            ruta_imagen = os.path.abspath('static/img/Publicaciones/'+str(session['id_user'])+'publication'+'/{0}'.format(img_name_new))
            ruta_bdd = 'static/img/Publicaciones/'+str(session['id_user'])+'publication'+'/{0}'.format(img_name_new)
            os.makedirs('static/img/Publicaciones/'+str(session['id_user'])+'publication', exist_ok=True)
            imgnewpub.save(ruta_imagen)
        else:
            ruta_bdd=str('static/img/imagenotfound.png')
        cur=mysql.connection.cursor()
        cur.execute("""CALL `INSERTpublication`('{0}', '{1}', '{2}', 1, {3})""".format(request.form['tittle'], request.form['txtdescription'], ruta_bdd, session["id_user"]))
        mysql.connection.commit()
        cur2=mysql.connection.cursor()
        cur2.execute("SELECT MAX(id) FROM publicacion")
        data=int(cur2.fetchall()[0][0])
    return redirect(url_for("seePublication",  pub=data))

@app.route('/editPublication', methods=["POST"])
def editPublication():
    data=[0]
    if(request.method=="POST"):
        ruta_bdd=''
        idpubedit=request.form["idpublicationedit"]
        tituloedit=request.form['tittle']
        txtdescedit=request.form['txtdescription']
        imgeditpub=request.files["imgpublication"]
        if(imgeditpub):
            img_name_new = secure_filename( 'a'+'_'+datetime.now().strftime('%d-%m-%Y %H_%M_%S')+'_.' + imgeditpub.filename.split('.')[-1])
            ruta_imagen = os.path.abspath('static/img/Publicaciones/'+str(session['id_user'])+'publication'+'/{0}'.format(img_name_new))
            ruta_bdd = 'static/img/Publicaciones/'+str(session['id_user'])+'publication'+'/{0}'.format(img_name_new)
            os.makedirs('static/img/Publicaciones/'+str(session['id_user'])+'publication', exist_ok=True)
            imgeditpub.save(ruta_imagen)
        else:
            cur=mysql.connection.cursor()
            cur.execute('SELECT url_archive FROM publicacion WHERE id={0}'.format(idpubedit))
            ruta_bdd=str(cur.fetchall()[0][0])
        cur2=mysql.connection.cursor()
        cur2.execute("""CALL `UPDATEpublication`('{0}', '{1}', '{2}',{3})""".format(tituloedit, txtdescedit, ruta_bdd,idpubedit))
        mysql.connection.commit()
    flash("Cambios realizados con exito", "edit")
    return redirect(url_for("seePublication", pub=idpubedit))

#Resive el id de la publicacion asi como la opcion, si se borrara o se pondra en privado
@app.route('/changeStatusPub/<string:idpubopt>')
def changeStatusPub(idpubopt):
    if(is_logged()):
        con=mysql.connection.cursor()
        consultaexistpub=''
        if(idpubopt.split('.')[1]=='3' and int(session["user_rol"])==2):
            consultaexistpub="""CALL `seePublication`({0},2)""".format(idpubopt.split('.')[0])
        else:
            consultaexistpub="""CALL `seePublication`({0},1)""".format(idpubopt.split('.')[0])
        con.execute(consultaexistpub)
        datapub=con.fetchall()
        if (datapub):
            if(int(datapub[0][5])==int(session["id_user"]) or int(session["user_rol"])==2):
                cur=mysql.connection.cursor()
                consulta=''
                mesagge=''
                if(idpubopt.split('.')[1]=='1'):
                    consulta="CALL `UPDATEstatusPublication`({0}, {1})".format(2, idpubopt.split('.')[0])
                    mesagge='Tu publicacion fue borrada con exito'
                elif(idpubopt.split('.')[1]=='2'):
                    consulta="CALL `UPDATEstatusPublication`({0}, {1})".format(3, idpubopt.split('.')[0])
                    mesagge='Se cambio la privacidad con exito. Ahora solo tu podras ver la publicacion'
                elif(idpubopt.split('.')[1]=='3'):
                    consulta="CALL `UPDATEstatusPublication`({0}, {1})".format(1, idpubopt.split('.')[0])
                    mesagge='Se cambio la privacidad con exito. Ahora todos podran ver la publicacion'
                elif(idpubopt.split('.')[1]=='4' and int(session['user_rol'])==2):
                    consulta="CALL `UPDATEstatusPublication`({0}, {1})".format(4, idpubopt.split('.')[0])
                    mesagge='Administrador elimino la publicacion con exito'
                cur.execute(consulta)
                mysql.connection.commit()
                if(idpubopt.split('.')[1]=='4' and int(session['user_rol'])==2):
                    cur1=mysql.connection.cursor()
                    cur1.execute("""CALL `seePublication`({0},2)""".format(idpubopt.split('.')[0]))
                    data2=cur1.fetchall()
                    return jsonify(mesagge=mesagge, newdelete=data2)
                elif (idpubopt.split('.')[1]=='3' and int(session['user_rol'])==2):
                    cur1=mysql.connection.cursor()
                    cur1.execute("""CALL `seePublication`({0},1)""".format(idpubopt.split('.')[0]))
                    data2=cur1.fetchall()
                    return jsonify(mesagge=mesagge, newdelete=data2)
                else:
                    return jsonify(mesagge=mesagge)
            else:
                return redirect(url_for('home'))
    else:
        return redirect(url_for('home'))
    

@app.route('/commentPub', methods=['POST'])
def commentPub():
    if(request.method=='POST'):
        idpub=int(request.form['idpublication'])
        if (is_logged()):
            
            cur=mysql.connection.cursor()
            cur.execute("CALL `INSERTcomment`('{0}', {1},{2})".format(request.form["txtcomment"],idpub, session["id_user"]))
            mysql.connection.commit()
        else:
            message='No puede comentar publicaciones si no has iniciado sesion en la pagina'
            messagetype='errorcomment'
            flash(message,messagetype)
    return redirect(url_for("seePublication", pub=idpub))

@app.route('/followUser/<string:idus_type>')
def followUser(idus_type):
    if(is_logged()):
        iduserfollow=int(idus_type.split('.')[0])
        cur=mysql.connection.cursor()
        cur.execute('SELECT * FROM reluserfollowuser WHERE iduserseguido={0} AND iduserquesigue={1}'.format(iduserfollow, session['id_user']))
        
        if(cur.fetchall()):
            cur2=mysql.connection.cursor()
            actualizacion=''
            if(idus_type.split('.')[1]=='follow'):
                cur2=mysql.connection.cursor()
                actualizacion="""CALL `UPDATEfollow`('{0}', {1},{2})""".format(1,iduserfollow, session['id_user'])
                
            else:
                actualizacion="""CALL `UPDATEfollow`('{0}', {1},{2})""".format(0,iduserfollow, session['id_user'])
            cur2.execute(actualizacion)
            mysql.connection.commit()
        else:
            cur3=mysql.connection.cursor()
            insercion=''
            if(idus_type.split('.')[1]=='follow'):
                insercion="""CALL `INSERTfollow`({0}, {1},{2})""".format(1,iduserfollow, session['id_user'])
            else:
                insercion="""CALL `INSERTfollow`({0}, {1},{2})""".format(0,iduserfollow, session['id_user'])
            cur3.execute(insercion)
            mysql.connection.commit()
        follow=True
    else:
        follow=False
    return jsonify(follow=follow)

@app.route('/messages/')
def messagesList():
    if (is_logged()):
        cur=mysql.connection.cursor()
        cur.execute("CALL `ConsultarConversaciones`({0})".format(session["id_user"]))
        data=cur.fetchall()

        cur2=mysql.connection.cursor()
        cur2.execute("CALL `ConsultarSeguidores`({0}, {1})".format(session["id_user"], 1))
        data2=cur2.fetchall()

        cur3=mysql.connection.cursor()
        cur3.execute("CALL `ConsultarSeguidores`({0}, {1})".format(session["id_user"], 2))
        data3=cur3.fetchall()
        return render_template('messages.html', conversaciones=data, seguidos=data3, seguidores=data2)
    else:
        flash('Debes estar logeado para ingresar a una conversacion','warning')
        return redirect(url_for('home'))

@app.route('/conversation/<idconvers>')
def conversation(idconvers):
    if (is_logged()):
        idconvers=int(idconvers)
        cur=mysql.connection.cursor()
        cur.execute("CALL `ConsultarMensajesConversacion`({0})".format(idconvers))
        data=cur.fetchall()
        data2=0
        if (data):
            if(int(data[0][1])==int(session["id_user"]) or int(data[0][2])==int(session["id_user"])):
                if(int(data[0][2])==int(session["id_user"])):
                    data2=data[0][1]
                else:
                    data2=data[0][2]
                cur2=mysql.connection.cursor()
                cur2.execute("CALL `ConsultarDatosUsuario`({0})".format(data2))
                data2=cur2.fetchall()[0]
            else:
                flash('No formas parte de este chat','warning')
                return redirect(url_for('home'))
        
        session['id_conversacion']=idconvers
        return render_template('conversation.html', messages=data, userdest=data2, idcon=idconvers)
    else:
        flash('Debes estar logeado para ingresar a una conversacion','warning')
        return redirect(url_for('home'))

@app.route('/createConversation/<iddestino>')
def createConversation(iddestino):
    if (is_logged()):
        iddestino=int(iddestino)
        cur=mysql.connection.cursor()
        cur.execute("CALL `CREATEconversacion`({0}, {1})".format(session["id_user"], iddestino))
        mysql.connection.commit()
        cur2=mysql.connection.cursor()
        cur2.execute('SELECT MAX(id) FROM conversacion where iduserremitente={0} and iduserdestino={1}'.format(session["id_user"], iddestino))
        data=cur2.fetchall()[0]
        return redirect(url_for('conversation', idconvers=data))
    else:
        flash('Debes estar logeado para ingresar a una conversacion','warning')
        return redirect(url_for('home'))

@socketiocon.on('message')
def handleMessage(msg, idsala, iduseremitente):
    print("El mensaje enviado es: "+msg+" enviado por el usuario: "+str(iduseremitente)+"en la conversacion "+str(session['id_conversacion']))
    cur=mysql.connection.cursor()
    cur.execute("CALL `INSERTmessage`('{0}', {1},{2})".format(msg, session["id_conversacion"], session["id_user"]))
    mysql.connection.commit()
    msg=msg+"."+str(iduseremitente)
    send(msg, to=idsala)

@socketiocon.on('userwriting')
def useriswriting(data):
    msg=['Esta escribiendo...',session["id_user"]]
    emit('userwriting',msg, to=data['room'])

@socketiocon.on('join')
def on_join(data):
    room = data["room"]
    
    print(data["room"])
    join_room(room)

@socketiocon.on('leave')
def leave(room):
    leave_room(room['room'])
    print(room["room"])

@socketiocon.on('disconnect')
def test_disconnect():
    leave_room(session['id_conversacion'])
    print('Client disconnected')

#Administrador
@app.route('/AdministratorPanel/<iduseradmin>')
def AdministratorPanel(iduseradmin):
    if(is_logged()):
        if(session['user_rol']==2):
            cur=mysql.connection.cursor()
            cur.execute("CALL `EstadisticasIndexAdmin`()")
            data=cur.fetchall()
            return render_template('PanelAdministrador/index.html', conteo=data)
        else:
            return redirect(url_for('home'))
    else:
            return redirect(url_for('home'))

@app.route('/getDataIndexAP/')
def getDataIndexAP():
    if(is_logged()):
        if(session['user_rol']==2):
            cur=mysql.connection.cursor()
            cur.execute("CALL `EtadGraficaIndexAP`()")
            data=cur.fetchall()
            cur2=mysql.connection.cursor()
            cur2.execute("CALL `EstNumUsersGenYNumPubsGen`('1')")
            data2=cur2.fetchall()
            cur3=mysql.connection.cursor()
            cur3.execute("CALL `EstNumUsersGenYNumPubsGen`('2')")
            data3=cur3.fetchall()
            return jsonify(datagraf=data, datagrafusers=data2, datagrafpubbygenero=data3)
        else:
            return redirect(url_for('home'))
    else:
            return redirect(url_for('home'))

@app.route('/reviewPosts/')
def reviewPosts():
    if(is_logged()):
        if(session['user_rol']==2):
            cur=mysql.connection.cursor()
            cur.execute("CALL `ConsultarPublicacionesAP`(1)")
            data=cur.fetchall()
            cur1=mysql.connection.cursor()
            cur1.execute("CALL `ConsultarPublicacionesAP`(2)")
            data2=cur1.fetchall()
            return render_template('PanelAdministrador/datatablePubs.html',publications=data, pubsdeleted=data2)
        else:
            return redirect(url_for('home'))
    else:
        return redirect(url_for('home'))
    

@app.route('/reviewUsers/')
def reviewUsers():
    if(is_logged()):
        if(session['user_rol']==2):
            cur=mysql.connection.cursor()
            cur.execute("CALL `ConsultarUsuariosAP`(1,0)")
            data=cur.fetchall()
            cur1=mysql.connection.cursor()
            cur1.execute("CALL `ConsultarUsuariosAP`(2,0)")
            data2=cur1.fetchall()
            return render_template('PanelAdministrador/datatableUsers.html',uactivedata=data, udelAdata=data2)
        else:
            return redirect(url_for('home'))
    else:
        return redirect(url_for('home'))
    
@app.route('/changeStatusUser/<string:iduseroption>')
def changeStatusUser(iduseroption):
    if(is_Admin()):
        cur=mysql.connection.cursor()
        cur.execute("CALL `UPDATEstatusUserAP`('{0}', '{1}')".format(iduseroption.split('.')[1], iduseroption.split('.')[0]))
        mysql.connection.commit()
        cur1=mysql.connection.cursor()
        cur1.execute("CALL `ConsultarUsuariosAP`(3,{0})".format(iduseroption.split('.')[0]))
        data=cur1.fetchall()
        return jsonify(userdataupd=data)
    else:
        return redirect(url_for('home'))


#rutas de juego
@app.route('/juegos')
def ShowGames():
    cur=mysql.connection.cursor()
    cur.execute("CALL `ConsultarPuntajes`()")
    data=cur.fetchall()
    datafacil=[]
    datanormal=[]
    datadificil=[]
    datalegfacil=[]
    datalegnormal=[]
    datalegdif=[]
    for puntaje in data:
        if(str(puntaje[5])=='Facil'):
            datafacil.append(puntaje)
        elif(str(puntaje[5])=='Normal'):
            datanormal.append(puntaje)
        elif(str(puntaje[5])=='Dificil'):
            datadificil.append(puntaje)
        elif(str(puntaje[5])=='Legendario Facil'):
            datalegfacil.append(puntaje)
        elif(str(puntaje[5])=='Legendario Normal'):
            datalegnormal.append(puntaje)
        elif(str(puntaje[5])=='Legendario Dificil'):
            datalegdif.append(puntaje)
    return render_template('juegos.html',facil=datafacil, normal=datanormal, dificil=datadificil, legfacil=datalegfacil, legnormal=datalegnormal,legdificil=datalegdif)
@app.route('/juegofractales/')
def juegoFractal():
    return render_template('fractales.html')

@app.route('/buscaminas/')
def buscaminas():
    return render_template('buscaminas.html')

@app.route('/puntajeGanador/<data>')
def puntajeGanador(data):
    if(is_logged()):
        data=data.split(',')
        if(int(data[2])<=50 and int(data[3])<=50):
            if(int(data[1])>=10 and int(data[1])<=19):
                dificultad='Facil'
            elif(int(data[1])>=20 and int(data[1])<=34):
                dificultad='Normal'
            else:
                dificultad='Dificil'
        elif(int(data[2])==100 and int(data[3])==100):
            if(int(data[1])>=10 and int(data[1])<=19):
                dificultad='Legendario Facil'
            elif(int(data[1])>=20 and int(data[1])<=34):
                dificultad='Legendario Normal'
            else:
                dificultad='Legendario Dificil'
            
        titlemensaje='Felicidades!'
        mensaje='Encontraste todas las minas en el tablero'
        typemsg='success'
        
        cur=mysql.connection.cursor()
        cur.execute("CALL `CREATEpuntaje`({0}, {1},{2},'{3}')".format(session["id_user"],data[0],data[1],dificultad))
        mysql.connection.commit()
    else:
        titlemensaje='Lo sentimos'
        mensaje='No podemos guardar tu puntaje si no estas logeado al sistema'
        typemsg='warning'
    return jsonify(message=mensaje,titlemessage=titlemensaje, messagetype=typemsg)

#Funciones de autentificacion de usuario
def is_logged():
    login = False
    if 'email' in session:
        login=True
    return login

def is_Admin():
    admin=False
    if (is_logged()):
        if(session['user_rol']==2):
            admin=True
    return admin

#Esta lineas son para indicar que metodos se podran llamar desde jinja2
app.jinja_env.globals.update(is_logged=is_logged)
#app.jinja_env.globals.update(=)
#app.jinja_env.globals.update(CloseSession=CloseSession)


##Evalua que el archivo que se esta ejecutando sea el main y no un modulo
if __name__=='__main__':
    #app.run(debug=True)##si es asi, se ejecuta la aplicacion
    #socketiocon.run(app, debug=True, host="192.168.1.66")
    socketiocon.run(app, debug=True)