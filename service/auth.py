import calendar
import datetime

import jwt
from flask_restx import abort

from constants import SECRET_KEY, ALGORITM
from service.user import UserService


class AuthService:
    def __init__(self, user_service: UserService):
        self.user_service = user_service

    def generate_tokens(self, username, password, is_reflash=False):
        user = self.user_service.get_one_username(username)

        if not user:
            raise abort(404)

        if not is_reflash:
            if not self.user_service.compare_passwords(user.password, password):
                return Exception()

        data = {
            "username": user.username,
            "role": user.role
        }

        min30 = datetime.datetime.utcnow() + datetime.timedelta(minutes=30)
        data["exp"] = calendar.timegm(min30.timetuple())
        access_token = jwt.encode(data, SECRET_KEY, algorithm=ALGORITM)
        days130 = datetime.datetime.utcnow() + datetime.timedelta(days=130)
        data["exp"] = calendar.timegm(days130.timetuple())
        refresh_token = jwt.encode(data, SECRET_KEY, algorithm=ALGORITM)
        tokens = {"access_token": access_token, "refresh_token": refresh_token}

        return tokens

    def approve_reflash_token(self, reflesh_token):
        data = jwt.decode(jwt=reflesh_token, key=SECRET_KEY, algorithms=ALGORITM)
        username = data['username']

        user = self.user_service.get_one_username(username)

        if not user:
            raise Exception()
        return self.generate_tokens(user.username, user.password, is_reflash=True)