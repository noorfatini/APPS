import jwt
from django.http import HttpResponseRedirect
from functools import wraps
from decouple import config
import os

def authenticate_request(view_func):
    @wraps(view_func)
    def wrapped_view(request, *args, **kwargs):
        token = request.COOKIES.get("Authorization")
        if not token:
            return HttpResponseRedirect("/login")

        # Debug print for JWT_SECRET
        # secret_key = os.getenv("POWERHR_JWT_SECRET")
        print("DEBUG: POWERHR_JWT_SECRET=", secret_key)

        secret_key = config('POWERHR_JWT_SECRET', default=None)
        if not secret_key:
            print("JWT secret key is not set. Ensure the environment variable is configured correctly.")
            return HttpResponseRedirect("/login")

        try:
            decoded_token = jwt.decode(token.split(" ")[1], secret_key, algorithms=["HS256"])
            request.token_user = {
                "email": decoded_token.get("email"),
                "role": decoded_token.get("role"),
                "name": decoded_token.get("name", f"{decoded_token.get('firstName')} {decoded_token.get('lastName')}")
            }
            return view_func(request, *args, **kwargs)
        except jwt.ExpiredSignatureError:
            return HttpResponseRedirect("/login")
        except jwt.InvalidTokenError:
            return HttpResponseRedirect("/login")
    return wrapped_view