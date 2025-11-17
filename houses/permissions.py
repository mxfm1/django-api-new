from rest_framework.permissions import BasePermission

class CanManageHouses(BasePermission):
    def has_permission(self,request,view):
        user = request.user

        if not user:
            return False
        
        if user.is_superuser:
            return True
        
        return request.method in ('GET',)
    
    def has_object_permission(self,request,view, obj):
        user = request.user

        if user.is_superuser:
            return True
        
        if user.is_staff:
            return obj.owner == user

        return request.method == "GET" and obj.owner == user        
    