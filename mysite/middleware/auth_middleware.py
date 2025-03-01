from django.utils.functional import SimpleLazyObject
from django.contrib.auth.models import AnonymousUser

class CustomUser:
    def __init__(self, session):
        self.is_authenticated = session.get("is_authenticated", False)
        self.email = session.get("user_email")
        self.name = session.get("user_name")
        self.role = session.get("user_role")
        self.id = session.get("user_id")

        # Add required attributes for Django admin and auth system
        self.is_active = session.get("is_active", True)  # Defaults to True
        self.is_staff = session.get("is_staff", False)   # Defaults to False
        self.is_superuser = session.get("is_superuser", False)  # Defaults to False

    def has_perm(self, perm, obj=None):
        return self.is_superuser

    def has_module_perms(self, app_label):
        return self.is_superuser

    def get_username(self):
        return self.email

    def __str__(self):
        return self.name or "Anonymous User"


def get_custom_user(request):
    if not hasattr(request, "_cached_custom_user"):
        if hasattr(request, "_dont_override_user") and request._dont_override_user:
            # Avoid overriding for superusers or fully authenticated users
            return request.user
        request._cached_custom_user = CustomUser(request.session)
    return request._cached_custom_user


class AuthenticationMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Set a flag to bypass middleware for superusers
        if hasattr(request, "user") and request.user.is_authenticated and request.user.is_superuser:
            request._dont_override_user = True
            print(f"DEBUG: Superuser detected. Middleware bypassed for user: {request.user}")
        else:
            # Set custom user
            request.user = SimpleLazyObject(lambda: get_custom_user(request))
            print(f"DEBUG: Middleware set custom user: {request.user}")
        return self.get_response(request)
