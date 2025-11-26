from rest_framework.permissions import AllowAny, BasePermission

from Users.users import choices


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
        
        if request.user.is_superuser:
            return True
        
        admin_profile = request.user.profiles.filter(
            type=choices.PROFILE_TYPE_ADMIN,
            status=choices.PROFILE_STATUS_ATIVO
        ).first()
        
        if admin_profile:
            return True
        
        owner_user = view.get_owner_user(obj)
        
        return owner_user == request.user
