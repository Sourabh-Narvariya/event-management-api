from rest_framework import permissions


class IsEventOrganizer(permissions.BasePermission):
    """
    Custom permission to only allow event organizers to edit their events.
    """
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.organizer == request.user


class IsReviewAuthor(permissions.BasePermission):
    """
    Custom permission to only allow review authors to edit or delete their reviews.
    """
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.author == request.user
