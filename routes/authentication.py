from utils.bdd import mysql
from flask import Blueprint, render_template, request, redirect, session, url_for, flash

authentication=Blueprint('authentication',__name__)

#Con esta se reenderiza la plnatilla de inicio de sesion y registro
@authentication.route('/SiginSignup/<string:option>')
def SiginSignup(option):
    if (is_logged()):
        return redirect(url_for('index.home'))
    else:
        if(option.upper()=='SIGNIN'):
            login='true'
            register='false'
        else:
            login='false'
            register='true'
        return render_template('loginregister.html', showlogin=login, showreg=register)

#Esta es para llevar a cabo el registro del usuario en la BDD y lo demas necesario
@authentication.route('/addUser', methods=['POST'])
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
            session["user_rol"]= 1
            mensaje = 'El usuario fue registrado exitosamente'
            messagetype='success'

        flash(mensaje,messagetype)
        return redirect(url_for('index.home'))
#Esta es para llevar a cabo el logeo del usuario comprobando en la BDD y creando las sessions
@authentication.route('/loginUser', methods=['POST'])
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
                return redirect(url_for('administrator.AdministratorPanel',iduseradmin=session["id_user"]))
            else:
                session['email'] = email
                
            messagetype='success'
        else:
            mensaje="Correo o Contrasena incorrectos intenta de nuevo"
            messagetype='warning'
        flash(mensaje, messagetype)
        return redirect(url_for('index.home'))

@authentication.route('/LogOut')
def LogOut():
    session['id_user']=None
    session['email'] = None
    session['password'] = None
    session['name'] = None    
    session['imgprofile'] = None
    session['id_conversacion']=None
    session['user_rol']=None  
    session.clear()
    return redirect(url_for('index.home'))

def is_logged():
    login = False
    if 'email' in session:
        login=True
    return login