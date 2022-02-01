from utils.bdd import mysql
from flask import Blueprint, jsonify, render_template, redirect, session, url_for

administrator=Blueprint('administrator',__name__)
#Administrador
@administrator.route('/AdministratorPanel/<iduseradmin>')
def AdministratorPanel(iduseradmin):
    if(is_logged()):
        if(session['user_rol']==2):
            cur=mysql.connection.cursor()
            cur.execute("CALL `EstadisticasIndexAdmin`()")
            data=cur.fetchall()
            return render_template('PanelAdministrador/index.html', conteo=data)
        else:
            return redirect(url_for('index.home'))
    else:
            return redirect(url_for('index.home'))

@administrator.route('/getDataIndexAP/')
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
            return redirect(url_for('idex.home'))
    else:
            return redirect(url_for('idex.home'))

@administrator.route('/reviewPosts/')
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
            return redirect(url_for('idex.home'))
    else:
        return redirect(url_for('idex.home'))
    

@administrator.route('/reviewUsers/')
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
            return redirect(url_for('idex.home'))
    else:
        return redirect(url_for('idex.home'))
    
@administrator.route('/changeStatusUser/<string:iduseroption>')
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
        return redirect(url_for('idex.home'))

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