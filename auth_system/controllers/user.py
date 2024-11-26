import pydash
from flask import jsonify, make_response, request

from auth_system import exceptions
from auth_system.logger import Logger
from auth_system.middleware.validation import auth_request
from auth_system.services.user import UserService


class UserController:
    @staticmethod
    @auth_request
    def create_user():
        try:
            data = request.json
            username = pydash.get(data, "username")
            password = pydash.get(data, "password")
            name = pydash.get(data, "name")
            lastName = pydash.get(data, "lastName")
            email = pydash.get(data, "email")

            result = UserService.create_user(username, password, name, lastName, email)

            return make_response(
                jsonify({"message": "User created", **result}),
                200,
            )

        except (
            exceptions.UserAlreadyExists,
            exceptions.UsernameTooLong,
            exceptions.UsernameTooShort,
            exceptions.PasswordTooLong,
            exceptions.PasswordTooShort,
        ) as e:
            return make_response(e.message, e.status_code)
        except Exception as e:
            Logger.error(e)
            return make_response(jsonify({"message": "Internal server error"}), 500)

    @staticmethod
    @auth_request
    def login_user():
        try:
            data = request.json
            username = pydash.get(data, "username")
            password = pydash.get(data, "password")

            result = UserService.login_user(username, password)

            return make_response(
                jsonify(
                    {
                        "message": "Login successfully",
                        **result,
                    }
                ),
                200,
            )

        except exceptions.InvalidCredentials as e:
            return make_response(e.message, e.status_code)
        except Exception as e:
            Logger.error(e)
            return make_response(jsonify({"message": "Internal server error"}), 500)
