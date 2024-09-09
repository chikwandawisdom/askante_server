from rest_framework import permissions


class IsTeacher(permissions.BasePermission):
    """
    Custom permission to only allow teachers to access the view.
    """

    def has_permission(self, request, view):
        return request.user.role == 'teacher'


class IsStudent(permissions.BasePermission):
    """
    Custom permission to only allow students to access the view.
    """

    def has_permission(self, request, view):
        return request.user.role == 'student'


class IsPublisher(permissions.BasePermission):
    """
    Custom permission to only allow publishers to access the view.
    """

    def has_permission(self, request, view):
        return request.user.role == 'publisher'


class IsSuperUser(permissions.BasePermission):
    """
    Custom permission to only allow superusers to access the view.
    """

    def has_permission(self, request, view):
        return request.user.is_superuser


class IsLibraryManager(permissions.BasePermission):
    """
    Custom permission to only allow library managers to access the view.
    """

    def has_permission(self, request, view):
        return request.user.special_role == 'librarian'


class IsBursar(permissions.BasePermission):
    """
    Custom permission to only allow bursars to access the view.
    """

    def has_permission(self, request, view):
        return request.user.special_role == 'bursar'
