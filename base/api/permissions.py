from rest_framework import permissions

"""class IsInGroupOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        # Check if the user is in a specific group
        return request.user and (
            request.user.is_superuser or request.user.groups.filter(name='Admins').exists()
        )
"""
class IsAuthenticated(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.path.startswith('/api/token'):
            return True
        if request.path.startswith('/api/'):
            return request.user.is_authenticated
        return True

class IsAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user and (
            request.user.groups.filter(name='Admin').exists()
        )

class IsAccountant(permissions.BasePermission):
    def has_permission(self, request, view):
        print('permission')
        return request.user and (
            request.user.groups.filter(name='Accountant').exists()
        )


"""class IsAccountantOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.role == 'Accountant' or request.user.role == 'Admin':
            return True
        return request.method in permissions.SAFE_METHODS

class IsWorkerOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.role == 'Worker' or request.user.role == 'Admin':
            return True
        return request.method in permissions.SAFE_METHODS"""
