from rest_framework.permissions import BasePermission

class IsOwnerOrReadOnly(BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.
    """
    
    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in self.SAFE_METHODS:
            return True
        
        # Write permissions are only allowed to the owner of the object.
        return obj.owner == request.user

class IsAdminUser(BasePermission):
    """
    Custom permission to only allow admin users to access the endpoint.
    """
    
    def has_permission(self, request, view):
        return request.user and request.user.is_staff

class IsAuthenticated(BasePermission):
    """
    Custom permission to only allow authenticated users to access the endpoint.
    """
    
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated