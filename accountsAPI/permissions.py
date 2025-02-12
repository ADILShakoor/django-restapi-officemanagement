from rest_framework import permissions

class CustomUserPermission(permissions.BasePermission):
    """
    Custom permission for user roles:
    - Super Admin: Can see all records.
    - Admin: Can see all records related to their company.
    - Team Lead: Can see all employees in their company.
    - Employee: Can only see their own record.
    """

    def has_permission(self, request, view):
        return request.user  and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        # Super Admin (can see everything)
        if request.user.is_superuser:
            return True

        # Admin (can see all users in the same company)
        if request.user.role == 'admin' or request.user.role=='ceo' and obj.company == request.user.company:
            if request.method in ['GET','PUT','PATCH']:
                return True
            return True

        # Team Lead (can see all employees in their company)
        if request.user.role == 'team_lead' and obj.role == 'employee' and obj.company == request.user.company:
            if request.method in ["GET","PUT","PATCH"]:
                return True
            return True # Deny access for delete 

        # Employee (can only see their own record)
        if request.user.role == 'employee' and obj == request.user:
            if request.method in ["GET","PUT","PATCH"]:
                return True
            return False    # Deny access for delete 

        return False     # Deny access for other cases
 