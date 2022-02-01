import base64
from datetime import datetime
import os
from utils.bdd import mysql
from flask import Blueprint, jsonify, render_template, request, redirect, session, url_for, flash

user = Blueprint("user", __name__)

@user.route('/UserProfile/<int:idprofile>')
def UserProfile(idprofile):
    data4=None
    if(is_logged()):
        if(int(session["id_user"])==idprofile):
            cur = mysql.connection.cursor()
            cur.execute("CALL `ConsultarDatosUsuario`({0})".format(session["id_user"]))
            data = cur.fetchall()[0]
            cur2 = mysql.connection.cursor()
            cur2.execute("""CALL `ConsultarPublicacionesDelPerfil`({0},{1})""".format(session["id_user"],0))
            data2 = cur2.fetchall()
            cur3 = mysql.connection.cursor()
            cur3.execute("""CALL `ConsultarLikesDelUsuario`({0},{1})""".format(session["id_user"],0))
            data3 = cur3.fetchall()
            cur4 = mysql.connection.cursor()
            cur4.execute("CALL `PrivatePubs`({0},{1})".format(session["id_user"],0))
            data4=cur4.fetchall()
            print('es tu perfil')
        else:
            cur = mysql.connection.cursor()
            cur.execute("""CALL `ConsultarOtroPerfilLogged`({0}, {1})""".format(idprofile, session["id_user"]))
            data = cur.fetchall()
            if(data):
                data=data[0]
                
            cur2 = mysql.connection.cursor()
            cur2.execute("""CALL `ConsultarPublicacionesDelPerfil`({0},{1})""".format(idprofile,0))
            data2 = cur2.fetchall()
            cur3 = mysql.connection.cursor()
            cur3.execute("""CALL `ConsultarLikesDelUsuario`({0},{1})""".format(idprofile,0))
            data3 = cur3.fetchall()
            print('no es tu peril')
    else:
        cur = mysql.connection.cursor()
        cur.execute("""CALL `ConsultarDatosUsuario`({0})""".format(idprofile))
        data = cur.fetchall()
        if(data):
            data=data[0]
        cur2 = mysql.connection.cursor()
        cur2.execute("""CALL `ConsultarPublicacionesDelPerfil`({0},{1})""".format(idprofile,0))
        data2 = cur2.fetchall()
        cur3 = mysql.connection.cursor()
        cur3.execute("""CALL `ConsultarLikesDelUsuario`({0},{1})""".format(idprofile,0))
        data3 = cur3.fetchall()
    return render_template('userprofile.html', userdata=data, userpubs = data2, userlikes = data3, userprivates = data4)

@user.route("/editProfile")
def editProfile():
    if(is_logged()):
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM usuario WHERE email='{0}'".format(session['email']))
        data = cur.fetchall()[0]
        return render_template("editprofile.html", userdata=data)
    else:
        return redirect(url_for('index.home'))

@user.route("/updateUser", methods=["POST"])
def updateUser():
    message=""
    messagetype=""
    ruta_bdd=""
    if request.method == 'POST':
        #time.sleep(10)
        emailedit = request.form["emailedit"]
        cur = mysql.connection.cursor()
        ##Esta es para obterner los registros donde se encuentre el mismo email, pero no el mismo id del usuario
        #es para evitar que al editar el correo usemos un correo que ya existe en otro usuario
        cur.execute("SELECT * FROM usuario WHERE email='{0}' AND id NOT LIKE {1}".format(emailedit, session['id_user']))
        if (cur.fetchall()):
            message="El correo que se ingreso ya esta siendo usado por otro usuario"
            messagetype="error"
        else:
            #se obtienen los demas datos
            firstnedit=request.form["firstnameedit"]
            lastnedit=request.form["lastnameedit"]
            passedit=request.form["passedit"]
            genderedit=request.form["generoedit"]
            dateedit=request.form["dateedit"]

            cur2 = mysql.connection.cursor()
            cur2.execute("""CALL `UPDATEuser`('{0}', '{1}','{2}','{3}','{4}','{5}',{6})
            """.format(firstnedit, lastnedit, emailedit, passedit, genderedit, dateedit, session['id_user']))
            mysql.connection.commit()
            message="Datos Actualizados Con Exito!"
            messagetype="success"
            #actualizamos las variables de sesion por posibles cambios
            session['email'] = emailedit
            session['password'] = passedit
            session['name'] = firstnedit
        flash(message, messagetype)
        return redirect(url_for("user.UserProfile", idprofile=int(session['id_user'])))
    
@user.route('/updateImgUserProfile', methods=["POST"])
def updateImgUserProfile():
    if request.method == 'POST':
        respuesta = request.get_json()
        imagennodecod = respuesta["image"]
        base64_img_bytes = imagennodecod.split(';base64,')[1].encode('utf-8')
        img_name_new = 'a'+'_'+datetime.now().strftime('%d-%m-%Y %H_%M_%S')+'_.jpg'
        ruta_imagen = 'static/img/'+str(session['id_user'])+'profile'+'/{0}'.format(img_name_new)
        ruta_bdd = 'static/img/'+str(session['id_user'])+'profile'+'/{0}'.format(img_name_new)
        os.makedirs('static/img/'+str(session['id_user'])+'profile', exist_ok=True)
        with open(ruta_imagen, 'wb') as file_to_save:
            imagen = base64.decodebytes(base64_img_bytes)
            file_to_save.write(imagen)
        cur1 = mysql.connection.cursor()
        cur1.execute("""CALL `UPDATEimgUserProfile`('{0}',{1})""".format(ruta_bdd, session['id_user']))
        mysql.connection.commit()
        session['imgprofile'] = ruta_bdd
        return jsonify(message="La imagen se recibio", file=ruta_bdd)
    else:
        return redirect(url_for('user.editProfile'))


@user.route('/followUser/<string:idus_type>')
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

def is_logged():
    login = False
    if 'email' in session:
        login=True
    return login