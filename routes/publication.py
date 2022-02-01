from datetime import datetime
import os
from utils.bdd import mysql
from werkzeug.utils import secure_filename
from flask import Blueprint, jsonify, render_template, request, redirect, session, url_for, flash

publication=Blueprint('publication',__name__)
#Cada que se use este tipo de rutas en flask, en el html antes de cada ruta de algun archivo agregar una /
#si no se agrega ocurre un error en el que al principio de la ruta se agrega el nombre de la ruta flask que
#se esta usando, por lo que las imagenes no se muestran
@publication.route("/publication/<int:pub>")
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

@publication.route('/like/<idpub>')
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

@publication.route('/crearPublicacion/<option>')
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
                    return redirect(url_for('index.home'))
            else:
                flash("No puedes editar publicaciones inexistentes o que fueron creadas por otro usuario", "warning")
                return redirect(url_for('index.home'))

        return render_template('crearPublicacion.html', datapub=data)
    else:
        flash("Debes iniciar sesion para poder crear una publicacion", "warning")
        return redirect(url_for('index.home'))

@publication.route('/addPublication', methods=["POST"])
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
    return redirect(url_for("publication.seePublication",  pub=data))

@publication.route('/editPublication', methods=["POST"])
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
    return redirect(url_for("publication.seePublication", pub=idpubedit))

#Resive el id de la publicacion asi como la opcion, si se borrara o se pondra en privado
@publication.route('/changeStatusPub/<string:idpubopt>')
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
                return redirect(url_for('index.home'))
    else:
        return redirect(url_for('index.home'))
    

@publication.route('/commentPub', methods=['POST'])
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
    return redirect(url_for("publication.seePublication", pub=idpub))


def is_logged():
    login = False
    if 'email' in session:
        login=True
    return login