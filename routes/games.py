from utils.bdd import mysql
from flask import Blueprint, jsonify, render_template, session

games = Blueprint("games", __name__)

#rutas de juego
@games.route('/juegos')
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


@games.route('/juegofractales/')
def juegoFractal():
    return render_template('fractales.html')

@games.route('/buscaminas/')
def buscaminas():
    return render_template('buscaminas.html')

@games.route('/puntajeGanador/<data>')
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

def is_logged():
    login = False
    if 'email' in session:
        login=True
    return login