from rest_framework.permissions import BasePermission, IsAuthenticated, SAFE_METHODS
from .models import Alert


class AlertPermission(BasePermission):
    message = 'Can not modify deleted alerts'

    def has_object_permission(self, request, view, obj: Alert):
        if not request.user == obj.user:
            self.message = 'Can not modify this object'
            return False
        if obj.status == Alert.DELETED:
            return request.method in SAFE_METHODS
        return True


IsAuthenticated = IsAuthenticated
