from flask import Blueprint, render_template

error=Blueprint('error', __name__)

##Manejo de errores
@error.errorhandler(404)
def handle_bad_request(e):
    return render_template('error404.html')