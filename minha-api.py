#!flask/bin/python
# -*- coding: UTF-8 -*-

from flask import Flask, jsonify, abort, make_response, request, url_for
from flask_restful import Api, Resource

from webargs import fields, validate
from webargs.flaskparser import use_args, use_kwargs, parser, abort

import werkzeug.exceptions as ex

import sys
import csv
import requests

#---------------------------------------

from flask_httpauth import HTTPBasicAuth
auth = HTTPBasicAuth()

app = Flask(__name__)
api = Api(app)

#-> Definição das variaveis necessarias

pacientes = []
lin = {}

pid = 0

#-> Lendo o CSV para a carregar a tabela

try:
    f = open('//home/marcos/workspace/api-rest/patients.csv', 'rb')
    csv_file = csv.reader(f)
except:
    raise ValueError('Ops!!! CSV não encontrado. Carga do dataset não foi efetuada, verifique...')

for row in csv_file:
    pid += 1
    lin['id']   = pid
    lin['nome'] = row
    pacientes.append(lin)
    lin = {}

f.close()

if pacientes:
    print ('Ok!!! Carga do dataset efetuada com sucesso...')
else:
    raise ValueError('Ops!!! Carga do dataset não foi efetuada, verifique...')

def make_public_paciente(paciente):
    new_paciente = {}
    for field in paciente:
        if field == 'id':
            new_paciente['uri'] = url_for('get_paciente', paciente_id=paciente['id'], _external=True)
        else:
            new_paciente[field] = paciente[field]
    return new_paciente


@auth.get_password
def get_password(username):
    if username == 'marcos':
        return 'python'
    return None

@auth.error_handler
def unauthorized():
    return make_response(jsonify({'Ops!!!': 'Unauthorized access'}), 403)


#----------------------------------
#-> 1. Listar todas os Pacientes...
#-> curl -u marcos:python -i http://localhost:8000/minha/api/v1.0/pacientes

@app.route('/minha/api/v1.0/pacientes', methods=['GET'])
#@auth.login_required
def get_pacientes():
    #return jsonify({'pacientes': pacientes})
    return jsonify({'pacientes': [make_public_paciente(paciente) for paciente in pacientes]})
#---------------------------------------------------------------------------------------------

#----------------------------------------------
#-> 2. Listar apenas um determinado Paciente...
#-> curl -u marcos:python -i http://localhost:8000/minha/api/v1.0/paciente/1

@app.route('/minha/api/v1.0/pacientes/<int:paciente_id>', methods=['GET'])
#@auth.login_required
def get_paciente(paciente_id):
    paciente = [paciente for paciente in pacientes if paciente['id'] == paciente_id]
    if len(paciente) == 0:
        abort(404)
    return jsonify({'paciente': paciente[0]})
#--------------------------------------------

#----------------------------------------------
#-> 3. Listar apenas um determinado Paciente...
#-> curl -u marcos:python -i http://localhost:8000/minha/api/v1.0/pacientenome/

@app.route('/minha/api/v1.0/pacientenome/<nome>', methods=['GET'])
#@auth.login_required
def get_nomepaciente(nome):
    paciente = [paciente for paciente in pacientes if paciente['nome'] == nome]
    if len(paciente) == 0:
        abort(404)
    return jsonify({'paciente': paciente[0]})

#@app.route('/user/<username>')
#def show_user(username):
#    user = User.query.filter_by(username=username).first_or_404()
#    return render_template('show_user.html', user=user)


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Ops!!! Record Not found...'}), 404)

if __name__ == '__main__':
    app.run(debug=True, port='8000')

