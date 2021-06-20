from functools import wraps

from flask import Response, jsonify
from flask_jwt_extended import verify_jwt_in_request, get_jwt


def roleCheck(role):
    def innerRole(func):
        @wraps(func)
        def decorator(*arguments, **keywordArguments):
            verify_jwt_in_request();
            claims = get_jwt();
            if (("role" in claims) and (role in claims["role"])):
                return func(*arguments, **keywordArguments);
            return jsonify(message="permission denied!"), 403;
        return decorator;
    return innerRole;
