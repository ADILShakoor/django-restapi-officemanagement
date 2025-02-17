from rest_framework import permissions

class CustomUserPermission(permissions.BasePermission):
   
    def has_permission(self, request, view):
        return request.user  and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        if request.user.is_superuser:
            return True
        if request.user.role == 'admin' or request.user.role=='ceo' and obj.company == request.user.company:
            if request.method in ['GET','PUT','PATCH']:
                return True
            return True
        if request.user.role == 'team_lead' and obj.role == 'employee' and obj.company == request.user.company:
            if request.method in ["GET","PUT","PATCH"]:
                return True
            return True # Deny access for delete 
        if request.user.role == 'employee' and obj == request.user:
            if request.method in ["GET","PUT","PATCH"]:
                return True
            return False    # Deny access for delete 

        return False     # Deny access for other cases
 