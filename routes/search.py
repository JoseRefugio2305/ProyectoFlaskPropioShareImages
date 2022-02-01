from utils.bdd import mysql
from flask import Blueprint, jsonify, render_template

search=Blueprint('search',__name__)
#Ruta json que funcionara para dar sugerencias y realizar la busqueda
@search.route('/SearchSuggestions/<string:opttext>')
def SearchSuggestions(opttext):
    opts=int(opttext.split('.')[0])
    textsearch=opttext.split('.')[1]
    cur=mysql.connection.cursor()
    if(opts==1):
        cur.execute("CALL `Busqueda`({0}, '{1}')".format(opts,textsearch))
        data=cur.fetchall()
    return jsonify(suger=data)

@search.route('/SearchResult/<string:opttextSearch>')
def Search(opttextSearch):
    optsearch=int(opttextSearch.split('.')[0])
    textSearch=opttextSearch.split('.')[1]
    ##el 2 corresponde a buscar en todas las publicaciones y todos lo usuarios
    if(optsearch==0):
        data=None
        data2=None
        return render_template('SearchResult.html', SearchPub=data, SearchUser=data2)
    elif(optsearch==2):
        cur=mysql.connection.cursor()
        cur.execute("CALL `Busqueda`({0}, '{1}')".format(2,textSearch))
        data=cur.fetchall()
        cur2=mysql.connection.cursor()
        cur2.execute("CALL `Busqueda`({0}, '{1}')".format(3,textSearch))##la opcion 3 corresponde a la busqueda de usuarios
        data2=cur2.fetchall()
        return render_template('SearchResult.html', SearchPub=data, SearchUser=data2)
    ##la opcion cuatro corresponde a la busqeda de las publicaciones propias y me gustas
    elif(optsearch==4):
        a=''