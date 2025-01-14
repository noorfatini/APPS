from django.utils.functional import SimpleLazyObject

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
        # Implement permission check logic, if applicable
        return self.is_superuser

    def has_module_perms(self, app_label):
        # Allow module-level permissions for superusers
        return self.is_superuser
    
    def get_username(self):
        """
        Return the username (or email) for the user.
        """
        return self.email

    def __str__(self):
        return self.name or "Anonymous User"

def get_custom_user(request):
    if not hasattr(request, "_custom_user"):
        request._custom_user = CustomUser(request.session)
    return request._custom_user

class AuthenticationMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        request.user = SimpleLazyObject(lambda: get_custom_user(request))
        print(f"DEBUG: Middleware user ID: {request.user.id}, Email: {request.user.email}")
        return self.get_response(request)
