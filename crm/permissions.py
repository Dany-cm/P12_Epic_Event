from rest_framework.permissions import BasePermission


class HasClientPermissions(BasePermission):

    def has_permission(self, request, view):
        return True

    def has_object_permission(self, request, view, obj):
        if request.user.groups.filter(name='sales'):
            if request.user == obj.sales_contact:
                return True
        return False


class HasContractPermissions(BasePermission):

    def has_permission(self, request, view):
        return True

    def has_object_permission(self, request, view, obj):
        if request.user.groups.filter(name='sales'):
            if request.user == obj.sales_contact:
                return True
        return False


class HasEventPermissions(BasePermission):

    def has_permission(self, request, view):
        return True

    def has_object_permission(self, request, view, obj):
        if request.user.groups.filter(name='supports'):
            if request.user == obj.support_contact:
                return True
        return False
