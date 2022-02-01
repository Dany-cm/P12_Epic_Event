from rest_framework.permissions import BasePermission, SAFE_METHODS


class HasClientPermissions(BasePermission):

    def has_permission(self, request, view):
        if request.user.groups.filter(name='supports'):
            return request.method in SAFE_METHODS
        return True

    def has_object_permission(self, request, view, obj):
        if request.user.groups.filter(name='sales'):
            if request.user == obj.sales_contact:
                return True

        if request.user.groups.filter(name='supports'):
            return request.method in SAFE_METHODS

        if request.user.groups.filter(name='managements'):
            return True
        return False


class HasContractPermissions(BasePermission):

    def has_permission(self, request, view):
        return True

    def has_object_permission(self, request, view, obj):
        if request.user.groups.filter(name='sales'):
            if request.user == obj.sales_contact:
                return True

        if request.user.groups.filter(name='managements'):
            return True
        return False


class HasEventPermissions(BasePermission):

    def has_permission(self, request, view):
        return True

    def has_object_permission(self, request, view, obj):
        if request.user.groups.filter(name='supports'):
            if request.user == obj.support_contact:
                return True

        if request.user.groups.filter(name='managements'):
            return True
        return False
