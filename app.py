import base64
from flask import Flask,render_template, request, redirect, session,url_for, flash, jsonify
from flask_mysqldb import MySQL
from flask_socketio import SocketIO, emit, join_room, leave_room, send
##Estos import pertenecen a las rutas de Blueprints
from routes.games import games
from routes.authentication import authentication
from routes.error import error
from routes.user import user
from routes.administrator import administrator
from routes.publication import publication
from routes.search import search
from routes.index import index
#Se importan configuraciones
from config import DATABASE_CONNECTION_DATA

app = Flask(__name__)

#Configuraciones de MySQL
#Siempre tener activado Laragon, y la BDD esta en MySQL
app.config['MYSQL_HOST']=DATABASE_CONNECTION_DATA[2]
app.config['MYSQL_USER']=DATABASE_CONNECTION_DATA[0]
app.config['MYSQL_PASSWORD']=DATABASE_CONNECTION_DATA[1]
app.config['MYSQL_DB']=DATABASE_CONNECTION_DATA[3]
mysql = MySQL(app)

#Session(app)

#Configuraciones de Sesion
app.secret_key = 'mysecretkey'

#configuraciones del socketio
socketiocon = SocketIO(app)

#Rutas de los mensajes
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
    #print("El mensaje enviado es: "+msg+" enviado por el usuario: "+str(iduseremitente)+"en la conversacion "+str(session['id_conversacion']))
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
    
    #print(data["room"])
    join_room(room)

@socketiocon.on('leave')
def leave(room):
    leave_room(room['room'])
    #print(room["room"])

@socketiocon.on('disconnect')
def test_disconnect():
    leave_room(session['id_conversacion'])
    #print('Client disconnected')

@app.route('/testimg')
def testimg():
    return render_template('testrecortarimg.html')

@app.route('/getimg', methods=["POST"])
def gettimg():
    respuesta = request.get_json()
    imagennodecod = respuesta["image"]
    base64_img_bytes = imagennodecod.split(';base64,')[1].encode('utf-8')
    
    with open('static/img/decoded_image.png', 'wb') as file_to_save:
        imagen = base64.decodebytes(base64_img_bytes)
        file_to_save.write(imagen)
    return jsonify(message="La imagen se recibio", file='gfg')


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

##Registro de Blueprints
app.register_blueprint(games)
app.register_blueprint(authentication)
app.register_blueprint(error)
app.register_blueprint(user)
app.register_blueprint(administrator)
app.register_blueprint(publication)
app.register_blueprint(search)
app.register_blueprint(index)





