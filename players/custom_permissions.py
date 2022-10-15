from rest_framework import permissions

class IsCurrentUserTeamMemberOrReadOnly(permissions.BasePermission):
    
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            
            # The method is a safe method
            return True
            
        else:
            return request.user.player in obj.players.all()

class IsCurrentPlayerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            # The method is a safe method
            return True
            
        else:
            return request.user.player is obj