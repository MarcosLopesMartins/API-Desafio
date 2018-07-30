#!flask/bin/python
# -*- coding: UTF-8 -*-

from models import Pessoas
from db import session
from datetime import datetime
from flask_restful import reqparse
from flask_restful import abort
from flask_restful import Resource
from flask_restful import fields
from flask_restful import marshal_with

pessoa_fields = {
    'id': fields.Integer,
    'nome': fields.String,
}

parser = reqparse.RequestParser()

class PacienteResource(Resource):
    @marshal_with(pessoa_fields)
    def get(self, id):
        pessoa = session.query(Pessoas).filter(passoa.id == id).first()
        if not note:
            abort(404, message="Ops!!! Paciente {} não existe...".format(id))
        return pessoa

class PacientesResource(Resource):
    @marshal_with(pessoa_fields)
    def get(self):
        pessoas = session.query(Pessoas).all()
        return pessoas

