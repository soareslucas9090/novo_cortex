from AppCore.core.permissions.permissions import AllowAnyPermission, IsOwnerOrAdminPermission


class AllowAnyMixin:
    permission_classes = [AllowAnyPermission]


class IsOwnerOrAdminMixin:
    permission_classes = [IsOwnerOrAdminPermission]
    
    def obter_usuario_dono(self, obj):
        raise NotImplementedError(
            f'{self.__class__.__name__} deve implementar o método obter_usuario_dono(obj)'
        )
