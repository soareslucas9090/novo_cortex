from rest_framework.permissions import AllowAny, BasePermission

from Usuarios.usuario import choices


class AllowAnyPermission(AllowAny):
    """
    Permissão que permite acesso a qualquer usuário, independentemente de autenticação.
    """
    pass


class IsOwnerOrAdminPermission(BasePermission):
    """
        Esta view permite que apenas o dono de um objeto ou um administrador acesse o recurso.
        Ela também permite acesso a qualquer usuário autenticado, mas restringe a ações que não interajam com nenhum objeto específico.
    """
    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        
        return True
    
    def has_object_permission(self, request, view, obj):
        if not request.user or not request.user.is_authenticated:
            return False
        
        if request.user.is_superuser or request.user.is_admin:
            return True
        
        usuario_proprietario = view.obter_usuario_dono(obj)
        
        return usuario_proprietario == request.user
