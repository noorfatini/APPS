import jwt
from django.http import HttpResponseRedirect
from functools import wraps
from decouple import config
import os


def token_user_context(request):
    """Context processor: exposes token_user info to all templates."""
    user_email = request.COOKIES.get("user_email")
    if user_email:
        return {
            'token_user': {
                "email": user_email,
                "role": request.COOKIES.get("user_role", ""),
                "name": request.COOKIES.get("user_name", ""),
            }
        }
    return {'token_user': None}


def authenticate_request(view_func):
    @wraps(view_func)
    def wrapped_view(request, *args, **kwargs):
        token = request.COOKIES.get("Authorization")
        user_email = request.COOKIES.get("user_email")

        if not token or not user_email:
            return HttpResponseRedirect("/login")

        # Validate JWT signature to ensure the token hasn't been tampered with
        secret_key = config('POWERHR_JWT_SECRET', default=None)
        if secret_key:
            try:
                jwt.decode(token.split(" ")[1], secret_key, algorithms=["HS256"])
            except jwt.ExpiredSignatureError:
                return HttpResponseRedirect("/login")
            except jwt.InvalidTokenError:
                return HttpResponseRedirect("/login")

        # PowerHR JWT payload only contains {id, type, company} — user info is in cookies
        request.token_user = {
            "email": user_email,
            "role": request.COOKIES.get("user_role", ""),
            "name": request.COOKIES.get("user_name", ""),
        }
        return view_func(request, *args, **kwargs)
    return wrapped_view