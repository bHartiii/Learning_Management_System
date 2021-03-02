from rest_framework import permissions
import enum

from Auth.models import Roles

SAFE_METHODS = ['GET', 'HEAD', 'OPTIONS']

class isAdmin(permissions.BasePermission):
    message = {'response': 'You are not an admin. Access Denied!'}

    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return request.META['user'].role == Roles.objects.get(role='mentor') or request.META['user'].role == Roles.objects.get(role='admin')
        else:
            return request.META['user'].role == Roles.objects.get(role='admin') or request.META['user'].is_superuser


class isMentorOrAdmin(permissions.BasePermission):
    message = {'response': 'You are not an Admin or a Mentor. Access Denied!'}

    def has_permission(self, request, view):
        return request.META['user'].role == Roles.objects.get(role='mentor') or request.META['user'].role == Roles.objects.get(role='admin')


class OnlyStudent(permissions.BasePermission):
    message = {'response': 'Only student can access'}

    def has_permission(self, request, view):
        return request.META['user'].role == Roles.objects.get(role='student')
