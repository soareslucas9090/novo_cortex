from AppCore.core.permissions.permissions import AllowAnyPermission, IsOwnerOrAdminPermission


class AllowAnyMixin:
    permission_classes = [AllowAnyPermission]


class IsOwnerOrAdminMixin:
    permission_classes = [IsOwnerOrAdminPermission]
    
    def get_owner_user(self, obj):
        raise NotImplementedError(
            f'{self.__class__.__name__} deve implementar o método get_owner_user(obj)'
        )
