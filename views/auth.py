from flask_restx import Namespace, Resource
from flask import request, abort

from implemented import auth_service

auth_ns = Namespace('auth')


@auth_ns.route('/')
class AuthView(Resource):
    def post(self):
        req_json = request.json
        username = req_json.get('username', None)
        password = req_json.get('password', None)
        if None in [username, password]:
            return '', 400

        tokens = auth_service.generate_tokens(username, password)

        return tokens, 201

    def put(self):
        req_json = request.json
        token = req_json.get('refrash_token')
        tokens = auth_service.approve_reflash_token(token)
        return tokens, 201
