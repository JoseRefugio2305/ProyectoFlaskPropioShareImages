from utils.bdd import mysql
from flask import Blueprint, jsonify, render_template,session

index=Blueprint('index',__name__)
#Rutas
@index.route('/')
def home():
    
    if (is_logged()):
        cur = mysql.connection.cursor()
        cur.execute("""CALL `ConsultarPublicacionesInicioLog`({0},{1})""".format(session["id_user"],0))
        data = cur.fetchall()
        #cur2 = mysql.connection.cursor()
        #cur2.execute("SELECT p.id FROM publicacion AS p INNER JOIN reluserreaction AS rur ON p.id=rur.idPub WHERE rur.idUser={0}".format(session["id_user"]))
        cur2=mysql.connection.cursor()
        cur2.execute("CALL `PublicacionesRelevantes`()")
        data2=cur2.fetchall()
    else:
        cur = mysql.connection.cursor()
        cur.execute("""CALL `ConsultarPublicacionesInicioNoLog`({0})""".format(0))
        data = cur.fetchall()

        cur2=mysql.connection.cursor()
        cur2.execute("""CALL `PublicacionesRelevantes`()""")
        data2=cur2.fetchall()
    
    return render_template('index.html', publications = data, relevantes=data2)


    

#Ruta json para traer otra tanda de publicaciones cuando se llegue al final
@index.route('/getMorePublics/<string:optcont>')
def getMorePublics(optcont):
    
    contador=int(optcont.split('.')[1])
    optionpage=int(optcont.split('.')[0])
    cur = mysql.connection.cursor()
    #print(optcont)
    if(optionpage==1):
        if(is_logged()):
            cur.execute("""CALL `ConsultarPublicacionesInicioLog`({0},{1})""".format(session["id_user"],contador))
            data = cur.fetchall()
            connecSistem=True
        else:
            cur.execute("""CALL `ConsultarPublicacionesInicioNoLog`({0})""".format(contador))
            data = cur.fetchall()
            connecSistem=False
        return jsonify(publications=data, is_connected=connecSistem)
    elif(optionpage==2):
        if(is_logged()):
            if(int(session["id_user"])==int(optcont.split('.')[2])):
                cur.execute("""CALL `ConsultarPublicacionesDelPerfil`({0},{1})""".format(session["id_user"],contador))
                data2 = cur.fetchall()
                connecSistem=True
            else:
                cur.execute("""CALL `ConsultarPublicacionesDelPerfil`({0},{1})""".format(int(optcont.split('.')[2]),contador))
                data2 = cur.fetchall()
                connecSistem=False
        else:
            cur.execute("""CALL `ConsultarPublicacionesDelPerfil`({0},{1})""".format(int(optcont.split('.')[2]),contador))
            data2 = cur.fetchall()
            connecSistem=False
        return jsonify(GroupPubs=data2, is_connected=connecSistem)
    elif(optionpage==3):
        if(is_logged()):
            if(int(session["id_user"])==int(optcont.split('.')[2])):
                cur.execute("CALL `PrivatePubs`({0},{1})".format(session["id_user"],contador))
                data2 = cur.fetchall()
                connecSistem=True
            else:
                data2=[]
                connecSistem=False
        else:
            data2=[]
            connecSistem=False
        return jsonify(GroupPubs=data2, is_connected=connecSistem)
    elif(optionpage==4):
        if(is_logged()):
            if(int(session["id_user"])==int(optcont.split('.')[2])):
                cur.execute("""CALL `ConsultarLikesDelUsuario`({0},{1})""".format(session["id_user"], contador))
                data2 = cur.fetchall()
                connecSistem=True
            else:
                cur.execute("""CALL `ConsultarLikesDelUsuario`({0},{1})""".format(session["id_user"],contador))
                data2 = cur.fetchall()
                connecSistem=True
        else:
            cur.execute("""CALL `ConsultarLikesDelUsuario`({0},{1})""".format(session["id_user"],contador))
            data2 = cur.fetchall()
            connecSistem=False
        return jsonify(GroupPubs=data2, is_connected=connecSistem)
    else:
        return jsonify(GroupPubs=[], is_connected=False)


def is_logged():
    login = False
    if 'email' in session:
        login=True
    return login