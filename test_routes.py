from flask import Blueprint

test=Blueprint('test',__name__)

@test.route('/test/')
def teste():
    return 'hola este es el test1'

@test.route('/test1/')
def testa():
    return 'hola este es el test2'