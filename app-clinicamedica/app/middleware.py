from django.core.exceptions import PermissionDenied


class AdministradorAdminMiddleware:
    """Impede que colaboradores/pacientes usem o Django Admin."""

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if (
            request.path.startswith("/admin/")
            and request.user.is_authenticated
            and not request.user.is_administrador
        ):
            raise PermissionDenied
        return self.get_response(request)
