from app import socketiocon, app
##Evalua que el archivo que se esta ejecutando sea el main y no un modulo
if __name__=='__main__':
    #app.run(debug=True)##si es asi, se ejecuta la aplicacion
    #socketiocon.run(app, debug=True, host="192.168.1.66")
    socketiocon.run(app, debug=True)